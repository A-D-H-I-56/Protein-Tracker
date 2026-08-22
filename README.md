# ⚡ NutriAI - Enterprise Fitness Nutrition & Protein Tracker

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![Architecture](https://img.shields.io/badge/Architecture-MVC%20%7C%20SOLID%20%7C%20DRY-purple.svg)](#architecture--design-patterns)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)](Dockerfile)

A production-grade, AI-driven personalized nutrition and macronutrient prediction platform. Powered by an optimized **Multi-Output k-Nearest Neighbors (k-NN) Regressor**, NutriAI delivers tailored caloric targets, exact protein, carb, and fat distributions, Mifflin-St Jeor metabolic baselines, structured 4-stage meal planning, and Explainable AI (XAI) nearest-neighbor distance matching.

---

## 🏛️ Architecture & Design Patterns

The codebase strictly adheres to **MVC (Model-View-Controller)** separation of concerns and **SOLID** software engineering principles:

```
Protein-Tracker/
├── .venv/                         # Isolated Virtual Environment
├── app/
│   ├── __init__.py                # Flask Application Factory (create_app)
│   ├── config.py                  # Environment-specific configuration (Dev/Test/Prod)
│   │
│   ├── models/                    # [M] MODEL LAYER (Domain entities & validation schemas)
│   │   ├── __init__.py
│   │   ├── user_profile.py        # UserProfile entity + Pydantic validation + BMR/TDEE formulas
│   │   ├── nutrition_plan.py      # NutritionPlan domain entity + macro ratios + meal entities
│   │   ├── ml_engine.py           # Thread-safe ML inference engine + k-NN nearest-neighbor XAI
│   │   └── metrics_model.py       # Benchmark metrics entity and metadata loader
│   │
│   ├── services/                  # BUSINESS LOGIC LAYER (Single Responsibility & Dependency Inversion)
│   │   ├── __init__.py
│   │   ├── nutrition_service.py   # Nutrition analytics + TDEE deltas + plan coordinator
│   │   ├── ml_service.py          # ML service facade decoupling controllers from ML persistence
│   │   └── meal_planner_service.py# Smart 4-stage meal distribution & food suggestions
│   │
│   ├── controllers/               # [C] CONTROLLER LAYER (Request handling & response dispatching)
│   │   ├── __init__.py
│   │   ├── web_controller.py      # Web page routes (/, /calculate, /metrics, /api-docs)
│   │   ├── api_controller.py      # RESTful API endpoints (/api/v1/predict, /api/v1/health, /api/v1/metrics, /api/v1/explain)
│   │   └── error_controller.py    # Centralized HTTP error handlers (400, 404, 500)
│   │
│   ├── static/                    # [V] VIEW ASSETS
│   │   ├── css/main.css           # Modern Glassmorphic CSS design system with Dark/Light mode tokens
│   │   ├── js/app.js              # Real-time biometric calculator, presets, theme switcher
│   │   └── js/charts.js           # Client-side interactive Chart.js visualizations
│   │
│   └── templates/                 # [V] VIEW TEMPLATES (Modular Jinja2)
│       ├── base.html              # Base layout with navbar, footer, theme switcher
│       ├── index.html             # Sleek calculator form with presets & live previews
│       ├── result.html            # Results dashboard with dynamic charts & XAI matches
│       ├── metrics.html           # Model evaluation & error distribution dashboard
│       ├── api_docs.html          # Interactive REST API documentation
│       └── errors/                # Error view templates (400, 404, 500)
│
├── ml_pipeline/                   # MACHINE LEARNING TRAINING & EVALUATION PIPELINE
│   ├── preprocess.py              # Data cleaning, sanitization & feature engineering
│   ├── train.py                   # Model training with cross-validation & artifact persistence
│   └── evaluate.py                # Visual residual analysis & diagnostic plot generation
│
├── tests/                         # AUTOMATED TEST SUITE
│   ├── test_models.py             # Unit tests for domain models & validation
│   ├── test_services.py           # Unit tests for business services
│   ├── test_controllers.py        # Integration tests for Web & REST API endpoints
│   └── test_ml_pipeline.py        # Tests for data preprocessing and training pipeline
│
├── artifacts/                     # Serialized Model Artifacts
│   ├── nutrition_model.pkl
│   ├── scaler.pkl
│   ├── label_encoders.pkl
│   ├── feature_names.json
│   └── evaluation_metrics.json
│
├── Fitness_data.csv               # Ground-truth fitness dataset (200 biometric instances)
├── run.py                         # Development entry point
├── wsgi.py                        # Production WSGI entry point (Waitress)
├── requirements.txt               # Pinned dependencies
├── .env.example                   # Environment configuration template
├── Dockerfile                     # Production container specification
├── docker-compose.yml             # Container orchestration
└── README.md                      # Documentation
```

---

## 🚀 Quickstart Guide

### 1. Prerequisites & Virtual Environment
```bash
# Clone the repository
git clone https://github.com/your-repo/Protein-Tracker.git
cd Protein-Tracker

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Train ML Model & Generate Evaluation Artifacts
```bash
python ml_pipeline/train.py
python ml_pipeline/evaluate.py
```

### 3. Run Development Server
```bash
python run.py
```
Open **[http://localhost:5000](http://localhost:5000)** in your browser.

### 4. Run Production WSGI Server
```bash
python wsgi.py
```

---

## 🧪 Automated Testing

Execute the complete unit and integration test suite:
```bash
pytest tests/ -v
```

---

## 📡 REST API Reference

### 1. Health Check
`GET /api/v1/health`
```json
{
  "model_loaded": true,
  "service": "Protein & Fitness Nutrition ML API",
  "status": "healthy",
  "version": "1.0.0"
}
```

### 2. Predict Nutrition Plan
`POST /api/v1/predict`
```bash
curl -X POST http://localhost:5000/api/v1/predict \
  -H "Content-Type: application/json" \
  -d '{
    "age": 25,
    "gender": "Male",
    "weight": 70.0,
    "height": 175.0,
    "activity_level": "Very Active",
    "goal": "Muscle Gain"
  }'
```

### 3. Model Benchmark Metrics
`GET /api/v1/metrics`

### 4. Explainable AI (k-NN Nearest Neighbors)
`POST /api/v1/explain?k=3`

---

## 🐳 Docker Deployment

```bash
# Build and run container
docker-compose up -d --build

# Check container health status
docker-compose ps
```

---

## ⚖️ License
Distributed under the MIT License.
