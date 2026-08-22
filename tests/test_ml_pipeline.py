import os
import pytest
from pathlib import Path
from ml_pipeline.preprocess import load_and_clean_data, prepare_features
from ml_pipeline.train import train_pipeline

def test_preprocess_and_clean_data():
    csv_path = "Fitness_data.csv"
    if not Path(csv_path).exists():
        pytest.skip("Fitness_data.csv not found")

    df = load_and_clean_data(csv_path)
    assert len(df) >= 200
    assert 'Age' in df.columns
    assert 'Weight' in df.columns
    assert 'Calories' in df.columns
    assert 'Protein' in df.columns
    assert 'Carbs' in df.columns
    assert 'Fat' in df.columns

    X, y, encoders = prepare_features(df)
    assert X.shape[1] == 6
    assert y.shape[1] == 4
    assert 'Gender' in encoders
    assert 'Activity_Level' in encoders
    assert 'Goal' in encoders

def test_train_pipeline_artifacts(tmp_path):
    csv_path = "Fitness_data.csv"
    if not Path(csv_path).exists():
        pytest.skip("Fitness_data.csv not found")

    temp_artifacts = tmp_path / "artifacts"
    model, scaler, encoders, metrics = train_pipeline(
        data_path=csv_path,
        artifacts_dir=str(temp_artifacts)
    )

    assert (temp_artifacts / 'nutrition_model.pkl').exists()
    assert (temp_artifacts / 'scaler.pkl').exists()
    assert (temp_artifacts / 'label_encoders.pkl').exists()
    assert (temp_artifacts / 'feature_names.json').exists()
    assert (temp_artifacts / 'evaluation_metrics.json').exists()

    assert 'Calories' in metrics
    assert 'Protein' in metrics
    assert metrics['Calories']['R2'] > 0.8
