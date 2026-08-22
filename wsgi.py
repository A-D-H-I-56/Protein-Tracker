import os
import logging
from pathlib import Path
from dotenv import load_dotenv
from waitress import serve

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(dotenv_path=BASE_DIR / '.env', override=False)

from app import create_app
from app.config import Config

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

app = create_app('production')

if __name__ == '__main__':
    host = Config.HOST
    port = Config.PORT
    threads = Config.THREADS
    
    logger.info(f"⚡ Serving NutriAI with Waitress WSGI on http://{host}:{port} (Threads={threads})")
    serve(app, host=host, port=port, threads=threads)
