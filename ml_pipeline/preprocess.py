import pandas as pd
import numpy as np
from typing import Tuple, Dict
from sklearn.preprocessing import StandardScaler, LabelEncoder

def load_and_clean_data(file_path: str) -> pd.DataFrame:
    """
    Load ground truth dataset from CSV and sanitize all numerical and categorical fields.
    """
    df = pd.read_csv(file_path)
    
    # Map varying header names to canonical schema
    column_mapping = {}
    for col in df.columns:
        c_lower = col.lower()
        if 'weight' in c_lower:
            column_mapping[col] = 'Weight'
        elif 'height' in c_lower:
            column_mapping[col] = 'Height'
        elif 'calories' in c_lower:
            column_mapping[col] = 'Calories'
        elif 'protein' in c_lower:
            column_mapping[col] = 'Protein'
        elif 'carbs' in c_lower or 'carbohydrate' in c_lower:
            column_mapping[col] = 'Carbs'
        elif 'fat' in c_lower:
            column_mapping[col] = 'Fat'
        elif 'activity' in c_lower:
            column_mapping[col] = 'Activity_Level'
        elif 'goal' in c_lower:
            column_mapping[col] = 'Goal'
        elif 'age' in c_lower:
            column_mapping[col] = 'Age'
        elif 'gender' in c_lower:
            column_mapping[col] = 'Gender'

    df = df.rename(columns=column_mapping)
    
    required_cols = ['Age', 'Gender', 'Weight', 'Height', 'Activity_Level', 'Goal', 'Calories', 'Protein', 'Carbs', 'Fat']
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Required column '{col}' missing from dataset.")

    df = df[required_cols]

    # Clean numeric columns (strip commas, convert to numeric, impute if necessary)
    numeric_cols = ['Age', 'Weight', 'Height', 'Calories', 'Protein', 'Carbs', 'Fat']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', ''), errors='coerce')
        if df[col].isna().sum() > 0:
            df[col] = df[col].fillna(df[col].median())

    # Clean and standardize categorical columns
    categorical_cols = ['Gender', 'Activity_Level', 'Goal']
    for col in categorical_cols:
        df[col] = df[col].astype(str).str.strip().str.title()

    df = df.dropna().reset_index(drop=True)
    return df

def prepare_features(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame, Dict[str, LabelEncoder]]:
    """
    Encode categorical features and separate into feature matrix X and target matrix y.
    """
    X = df[['Age', 'Gender', 'Weight', 'Height', 'Activity_Level', 'Goal']].copy()
    y = df[['Calories', 'Protein', 'Carbs', 'Fat']].copy()

    label_encoders = {}
    for col in ['Gender', 'Activity_Level', 'Goal']:
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col])
        label_encoders[col] = le

    return X, y, label_encoders
