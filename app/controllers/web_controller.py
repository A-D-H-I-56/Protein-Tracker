from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from pydantic import ValidationError
from app.models.user_profile import UserProfile
from app.services.nutrition_service import NutritionService
from app.services.ml_service import MLService

web_bp = Blueprint('web', __name__)

def get_services():
    """Retrieve services from application context or factory."""
    artifacts_dir = current_app.config['ARTIFACTS_DIR']
    dataset_path = current_app.config['DATASET_PATH']
    ml_service = MLService(artifacts_dir=artifacts_dir, dataset_path=dataset_path)
    nutrition_service = NutritionService(ml_service=ml_service)
    return ml_service, nutrition_service

@web_bp.route('/', methods=['GET'])
def index():
    """Render the interactive nutrition calculator landing page."""
    return render_template('index.html')

@web_bp.route('/calculate', methods=['POST'])
def calculate():
    """Handle form submission, validate input with UserProfile domain model, and display results."""
    ml_service, nutrition_service = get_services()

    if not ml_service.is_ready:
        return render_template(
            'result.html',
            error="ML model is currently unavailable or artifacts are missing. Please ensure training has been executed."
        ), 503

    try:
        raw_data = {
            'age': request.form.get('age'),
            'gender': request.form.get('gender'),
            'weight': request.form.get('weight'),
            'height': request.form.get('height'),
            'activity_level': request.form.get('activity_level'),
            'goal': request.form.get('goal')
        }

        # Domain Validation with Pydantic
        profile = UserProfile(**raw_data)

        # Service Calculation
        plan = nutrition_service.calculate_plan(profile)
        metrics = ml_service.get_metrics()

        return render_template(
            'result.html',
            profile=profile,
            plan=plan,
            metrics=metrics
        )
    except ValidationError as ve:
        error_msgs = [f"{err['loc'][0]}: {err['msg']}" for err in ve.errors()]
        return render_template('result.html', error="Validation Error: " + "; ".join(error_msgs)), 400
    except Exception as e:
        current_app.logger.error(f"Prediction error: {e}", exc_info=True)
        return render_template('result.html', error=f"An unexpected calculation error occurred: {str(e)}"), 500

@web_bp.route('/metrics', methods=['GET'])
def metrics():
    """Render the production ML model evaluation and diagnostics page."""
    ml_service, _ = get_services()
    model_metrics = ml_service.get_metrics()
    return render_template('metrics.html', metrics=model_metrics)

@web_bp.route('/api-docs', methods=['GET'])
def api_docs():
    """Render interactive REST API documentation."""
    return render_template('api_docs.html')
