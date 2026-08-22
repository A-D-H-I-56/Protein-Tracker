import json
import logging
from pathlib import Path
from typing import Dict, Any, List, Tuple
import joblib
import numpy as np
import pandas as pd
from app.models.nutrition_plan import SimilarProfile

logger = logging.getLogger(__name__)

class MLEngine:
    """
    Production-grade ML Inference and Explainability Engine.
    Encapsulates model loading, feature transformations, prediction,
    and k-NN nearest-neighbor similarity searches.
    """
    def __init__(self, artifacts_dir: Path, dataset_path: Path):
        self.artifacts_dir = Path(artifacts_dir)
        self.dataset_path = Path(dataset_path)
        self.model = None
        self.scaler = None
        self.label_encoders = None
        self.feature_names = None
        self.dataset_df = None
        self.is_loaded = False
        
        self.load_artifacts()

    def load_artifacts(self) -> bool:
        """Load all serialized artifacts into memory."""
        try:
            model_path = self.artifacts_dir / 'nutrition_model.pkl'
            scaler_path = self.artifacts_dir / 'scaler.pkl'
            encoders_path = self.artifacts_dir / 'label_encoders.pkl'
            features_path = self.artifacts_dir / 'feature_names.json'

            if not model_path.exists():
                logger.warning(f"Model file not found at {model_path}. Please run training pipeline.")
                return False

            self.model = joblib.load(model_path)
            self.scaler = joblib.load(scaler_path)
            self.label_encoders = joblib.load(encoders_path)

            with open(features_path, 'r') as f:
                self.feature_names = json.load(f)

            if self.dataset_path.exists():
                df = pd.read_csv(self.dataset_path)
                # Normalize column names
                col_map = {
                    'Age': 'Age', 'Gender': 'Gender', 'Weight (kg)': 'Weight', 'Height (cm)': 'Height',
                    'Activity Level': 'Activity_Level', 'Goal': 'Goal', 'Calories (kcal)': 'Calories',
                    'Protein (g)': 'Protein', 'Carbs (g)': 'Carbs', 'Fat (g)': 'Fat'
                }
                self.dataset_df = df.rename(columns={k: v for k, v in col_map.items() if k in df.columns})
                # Clean numeric columns
                for col in ['Calories', 'Protein', 'Carbs', 'Fat']:
                    if col in self.dataset_df.columns:
                        self.dataset_df[col] = pd.to_numeric(
                            self.dataset_df[col].astype(str).str.replace(',', ''), errors='coerce'
                        )

            self.is_loaded = True
            logger.info("MLEngine loaded successfully.")
            return True
        except Exception as e:
            logger.error(f"Failed to load ML artifacts: {e}", exc_info=True)
            self.is_loaded = False
            return False

    def transform_features(self, profile_dict: Dict[str, Any]) -> Tuple[pd.DataFrame, np.ndarray]:
        """Prepares and scales features for model inference."""
        if not self.is_loaded:
            raise RuntimeError("MLEngine is not initialized with valid model artifacts.")

        df = pd.DataFrame([{
            'Age': profile_dict['age'],
            'Gender': profile_dict['gender'],
            'Weight': profile_dict['weight'],
            'Height': profile_dict['height'],
            'Activity_Level': profile_dict['activity_level'],
            'Goal': profile_dict['goal']
        }])

        # Apply label encoders
        for col in ['Gender', 'Activity_Level', 'Goal']:
            if col in self.label_encoders:
                le = self.label_encoders[col]
                val = df[col].iloc[0]
                if val not in le.classes_:
                    raise ValueError(f"Unknown value '{val}' for categorical feature '{col}'")
                df[col] = le.transform([val])[0]

        df = df[self.feature_names]
        scaled = self.scaler.transform(df)
        return df, scaled

    def predict(self, profile_dict: Dict[str, Any]) -> Dict[str, int]:
        """Execute regression prediction on user profile."""
        _, scaled_input = self.transform_features(profile_dict)
        raw_pred = self.model.predict(scaled_input)[0]

        calories = max(800, min(6000, int(round(raw_pred[0]))))
        protein = max(30, min(400, int(round(raw_pred[1]))))
        carbs = max(20, min(800, int(round(raw_pred[2]))))
        fat = max(15, min(300, int(round(raw_pred[3]))))

        return {
            'calories': calories,
            'protein': protein,
            'carbs': carbs,
            'fat': fat
        }

    def find_similar_profiles(self, profile_dict: Dict[str, Any], k: int = 3) -> List[SimilarProfile]:
        """
        Find top K most similar fitness profiles using k-NN distance in scaled feature space.
        Provides explainable AI (XAI) insights.
        """
        if not self.is_loaded or self.dataset_df is None:
            return []

        try:
            _, scaled_input = self.transform_features(profile_dict)

            # Extract features from training dataset and transform
            feature_df = self.dataset_df[['Age', 'Gender', 'Weight', 'Height', 'Activity_Level', 'Goal']].copy()
            for col in ['Gender', 'Activity_Level', 'Goal']:
                if col in self.label_encoders:
                    le = self.label_encoders[col]
                    feature_df[col] = feature_df[col].apply(lambda v: le.transform([v])[0] if v in le.classes_ else 0)

            dataset_scaled = self.scaler.transform(feature_df[self.feature_names])
            distances = np.linalg.norm(dataset_scaled - scaled_input, axis=1)

            top_indices = np.argsort(distances)[:k]
            similar_profiles = []

            for idx in top_indices:
                row = self.dataset_df.iloc[idx]
                dist = distances[idx]
                # Convert Euclidean distance to 0-100% similarity score
                similarity = round(max(0.0, 100.0 * (1.0 / (1.0 + dist))), 1)

                similar_profiles.append(SimilarProfile(
                    similarity_score=similarity,
                    age=int(row['Age']),
                    gender=str(row['Gender']),
                    weight=float(row['Weight']),
                    height=float(row['Height']),
                    activity_level=str(row['Activity_Level']),
                    goal=str(row['Goal']),
                    calories=int(row['Calories']),
                    protein=int(row['Protein']),
                    carbs=int(row['Carbs']),
                    fat=int(row['Fat'])
                ))

            return similar_profiles
        except Exception as e:
            logger.warning(f"Error computing nearest neighbors: {e}")
            return []
