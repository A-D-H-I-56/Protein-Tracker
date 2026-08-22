import os
import logging
from waitress import serve
from app import create_app

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

app = create_app('production')

if __name__ == '__main__':
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 5000))
    threads = int(os.environ.get('THREADS', 4))
    
    logger.info(f"⚡ Serving NutriAI with Waitress WSGI on http://{host}:{port} (Threads={threads})")
    serve(app, host=host, port=port, threads=threads)
