import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

class Config:
    """Base application configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'protein-tracker-dev-key-2026-secure')
    ARTIFACTS_DIR = os.environ.get('ARTIFACTS_DIR', str(BASE_DIR / 'artifacts'))
    DATASET_PATH = os.environ.get('DATASET_PATH', str(BASE_DIR / 'Fitness_data.csv'))
    STATIC_FOLDER = str(BASE_DIR / 'app' / 'static')
    TEMPLATES_FOLDER = str(BASE_DIR / 'app' / 'templates')
    
    # ML Engine Settings
    KNN_NEIGHBORS = 5
    KNN_METRIC = 'euclidean'
    
    # Validation Boundaries
    MIN_AGE = 15
    MAX_AGE = 100
    MIN_WEIGHT = 40.0
    MAX_WEIGHT = 200.0
    MIN_HEIGHT = 140.0
    MAX_HEIGHT = 220.0
    
    # Allowed Categoricals
    ALLOWED_GENDERS = ['Male', 'Female']
    ALLOWED_ACTIVITY_LEVELS = ['Sedentary', 'Light Active', 'Active', 'Very Active']
    ALLOWED_GOALS = ['Weight Loss', 'Maintenance', 'Muscle Gain']

class DevelopmentConfig(Config):
    """Development environment configuration."""
    DEBUG = True
    TESTING = False

class TestingConfig(Config):
    """Testing environment configuration."""
    DEBUG = False
    TESTING = True
    ARTIFACTS_DIR = str(BASE_DIR / 'artifacts')

class ProductionConfig(Config):
    """Production environment configuration."""
    DEBUG = False
    TESTING = False

config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
