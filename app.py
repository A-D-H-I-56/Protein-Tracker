"""
NutriAI - Main Application Entrypoint
Provides backward compatibility for direct `python app.py` execution
while routing through the production Application Factory and MVC architecture.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(dotenv_path=BASE_DIR / '.env', override=False)

from app import create_app
from app.config import Config

app = create_app(Config.FLASK_ENV)

if __name__ == '__main__':
    host = Config.HOST
    port = Config.PORT
    print(f"🚀 Starting NutriAI Fitness Nutrition Calculator at http://{host}:{port}")
    app.run(host=host, port=port, debug=(Config.FLASK_ENV == 'development'))