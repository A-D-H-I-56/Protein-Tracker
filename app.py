"""
NutriAI - Main Application Entrypoint
Provides backward compatibility for direct `python app.py` execution
while routing through the production Application Factory and MVC architecture.
"""
import os
from app import create_app

app = create_app(os.environ.get('FLASK_ENV', 'development'))

if __name__ == '__main__':
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 5000))
    print(f"🚀 Starting NutriAI Fitness Nutrition Calculator at http://{host}:{port}")
    app.run(host=host, port=port, debug=True)