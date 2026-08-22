import os
import sys
from pathlib import Path

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

import json
import logging
import joblib
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from ml_pipeline.preprocess import load_and_clean_data, prepare_features

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

def train_pipeline(data_path: str = "Fitness_data.csv", artifacts_dir: str = "artifacts"):
    """
    Automated training pipeline for the Fitness Nutrition k-NN regression model.
    """
    artifacts_path = Path(artifacts_dir)
    artifacts_path.mkdir(parents=True, exist_ok=True)

    logger.info(f"Loading dataset from {data_path}...")
    df = load_and_clean_data(data_path)
    logger.info(f"Dataset sanitized successfully. Shape: {df.shape}")

    X, y, label_encoders = prepare_features(df)
    feature_names = list(X.columns)
    target_names = list(y.columns)

    # Train/Test Split (120 train, 80 test for 200 rows)
    train_size = min(120, int(len(df) * 0.6))
    test_size = len(df) - train_size
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, train_size=train_size, random_state=42
    )

    logger.info(f"Data Split: {len(X_train)} train samples, {len(X_test)} test samples.")

    # Feature Scaling
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Model Fitting
    logger.info("Training KNeighborsRegressor (k=5, metric=euclidean)...")
    model = KNeighborsRegressor(n_neighbors=5, metric='euclidean', weights='distance')
    model.fit(X_train_scaled, y_train)

    # Evaluation
    y_pred = model.predict(X_test_scaled)
    metrics = {}
    for i, target in enumerate(target_names):
        mae = float(mean_absolute_error(y_test.iloc[:, i], y_pred[:, i]))
        mse = float(mean_squared_error(y_test.iloc[:, i], y_pred[:, i]))
        rmse = float(np.sqrt(mse))
        r2 = float(r2_score(y_test.iloc[:, i], y_pred[:, i]))
        metrics[target] = {
            'MAE': round(mae, 4),
            'MSE': round(mse, 4),
            'RMSE': round(rmse, 4),
            'R2': round(r2, 4)
        }
        logger.info(f"Target '{target}': MAE={mae:.2f}, RMSE={rmse:.2f}, R2={r2:.4f}")

    # Persist Artifacts
    logger.info(f"Persisting model artifacts to {artifacts_path.resolve()}...")
    joblib.dump(model, artifacts_path / 'nutrition_model.pkl')
    joblib.dump(scaler, artifacts_path / 'scaler.pkl')
    joblib.dump(label_encoders, artifacts_path / 'label_encoders.pkl')
    joblib.dump({'X_test': X_test, 'y_test': y_test, 'y_pred': y_pred, 'target_names': target_names}, artifacts_path / 'test_sets.pkl')

    with open(artifacts_path / 'feature_names.json', 'w') as f:
        json.dump(feature_names, f, indent=4)

    with open(artifacts_path / 'evaluation_metrics.json', 'w') as f:
        json.dump(metrics, f, indent=4)

    logger.info("Training pipeline finished successfully!")
    return model, scaler, label_encoders, metrics

if __name__ == "__main__":
    train_pipeline()
