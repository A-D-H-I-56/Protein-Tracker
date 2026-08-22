import os
from app import create_app

app = create_app(os.environ.get('FLASK_ENV', 'development'))

if __name__ == '__main__':
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 5000))
    print(f"🚀 Launching NutriAI Development Server at http://{host}:{port}")
    app.run(host=host, port=port, debug=True)
