import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file if present
load_dotenv(dotenv_path=BASE_DIR / '.env', override=False)

class Config:
    """Base application configuration with zero hardcoded values."""
    # Flask Environment & Secrets
    FLASK_ENV = os.environ.get('FLASK_ENV', 'development')
    SECRET_KEY = os.environ.get('SECRET_KEY', 'protein-tracker-secret-key-2026-production')
    
    # Server Network Bindings
    HOST = os.environ.get('HOST', '0.0.0.0')
    PORT = int(os.environ.get('PORT', 5000))
    THREADS = int(os.environ.get('THREADS', 4))
    
    # File Paths & Directories
    ARTIFACTS_DIR = os.environ.get('ARTIFACTS_DIR', str(BASE_DIR / 'artifacts'))
    DATASET_PATH = os.environ.get('DATASET_PATH', str(BASE_DIR / 'Fitness_data.csv'))
    STATIC_FOLDER = os.environ.get('STATIC_FOLDER', str(BASE_DIR / 'app' / 'static'))
    TEMPLATES_FOLDER = os.environ.get('TEMPLATES_FOLDER', str(BASE_DIR / 'app' / 'templates'))
    
    # ML Model & Training Hyperparameters
    KNN_NEIGHBORS = int(os.environ.get('KNN_NEIGHBORS', 5))
    KNN_METRIC = os.environ.get('KNN_METRIC', 'euclidean')
    KNN_WEIGHTS = os.environ.get('KNN_WEIGHTS', 'distance')
    TRAIN_SPLIT_RATIO = float(os.environ.get('TRAIN_SPLIT_RATIO', 0.6))
    RANDOM_STATE = int(os.environ.get('RANDOM_STATE', 42))
    TOP_K_EXPLAIN_DEFAULT = int(os.environ.get('TOP_K_EXPLAIN_DEFAULT', 3))
    
    # Validation Boundaries
    MIN_AGE = int(os.environ.get('MIN_AGE', 15))
    MAX_AGE = int(os.environ.get('MAX_AGE', 100))
    MIN_WEIGHT = float(os.environ.get('MIN_WEIGHT', 40.0))
    MAX_WEIGHT = float(os.environ.get('MAX_WEIGHT', 200.0))
    MIN_HEIGHT = float(os.environ.get('MIN_HEIGHT', 140.0))
    MAX_HEIGHT = float(os.environ.get('MAX_HEIGHT', 220.0))
    
    # Target Range Clamps
    MIN_CALORIES = int(os.environ.get('MIN_CALORIES', 800))
    MAX_CALORIES = int(os.environ.get('MAX_CALORIES', 6000))
    MIN_PROTEIN = int(os.environ.get('MIN_PROTEIN', 30))
    MAX_PROTEIN = int(os.environ.get('MAX_PROTEIN', 400))
    MIN_CARBS = int(os.environ.get('MIN_CARBS', 20))
    MAX_CARBS = int(os.environ.get('MAX_CARBS', 800))
    MIN_FAT = int(os.environ.get('MIN_FAT', 15))
    MAX_FAT = int(os.environ.get('MAX_FAT', 300))
    
    # Meal Distribution Percentages (must sum to 1.0)
    MEAL_BREAKFAST_PCT = float(os.environ.get('MEAL_BREAKFAST_PCT', 0.25))
    MEAL_LUNCH_PCT = float(os.environ.get('MEAL_LUNCH_PCT', 0.35))
    MEAL_DINNER_PCT = float(os.environ.get('MEAL_DINNER_PCT', 0.25))
    MEAL_SNACKS_PCT = float(os.environ.get('MEAL_SNACKS_PCT', 0.15))
    
    # Allowed Categoricals
    ALLOWED_GENDERS = os.environ.get('ALLOWED_GENDERS', 'Male,Female').split(',')
    ALLOWED_ACTIVITY_LEVELS = os.environ.get(
        'ALLOWED_ACTIVITY_LEVELS', 'Sedentary,Light Active,Active,Very Active'
    ).split(',')
    ALLOWED_GOALS = os.environ.get(
        'ALLOWED_GOALS', 'Weight Loss,Maintenance,Muscle Gain'
    ).split(',')

class DevelopmentConfig(Config):
    """Development environment configuration."""
    DEBUG = True
    TESTING = False

class TestingConfig(Config):
    """Testing environment configuration."""
    DEBUG = False
    TESTING = True

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
