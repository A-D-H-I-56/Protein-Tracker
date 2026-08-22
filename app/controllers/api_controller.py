from flask import Blueprint, request, jsonify, current_app
from pydantic import ValidationError
from app.models.user_profile import UserProfile
from app.services.nutrition_service import NutritionService
from app.services.ml_service import MLService

api_bp = Blueprint('api', __name__, url_prefix='/api/v1')

def get_services():
    artifacts_dir = current_app.config['ARTIFACTS_DIR']
    dataset_path = current_app.config['DATASET_PATH']
    ml_service = MLService(artifacts_dir=artifacts_dir, dataset_path=dataset_path)
    nutrition_service = NutritionService(ml_service=ml_service)
    return ml_service, nutrition_service

@api_bp.route('/health', methods=['GET'])
def health():
    """Health check endpoint providing service status and model availability."""
    ml_service, _ = get_services()
    status = "healthy" if ml_service.is_ready else "degraded"
    return jsonify({
        "status": status,
        "model_loaded": ml_service.is_ready,
        "version": "1.0.0",
        "service": "Protein & Fitness Nutrition ML API"
    }), 200 if ml_service.is_ready else 503

@api_bp.route('/predict', methods=['POST'])
def predict():
    """
    REST API endpoint for personalized nutrition recommendation.
    Accepts JSON with: age, gender, weight, height, activity_level, goal.
    """
    if not request.is_json:
        return jsonify({"error": "Request payload must be JSON with Content-Type: application/json"}), 415

    ml_service, nutrition_service = get_services()
    if not ml_service.is_ready:
        return jsonify({"error": "ML Model is not ready or artifacts missing"}), 503

    try:
        data = request.get_json()
        profile = UserProfile(**data)
        plan = nutrition_service.calculate_plan(profile)

        response = {
            "success": True,
            "data": {
                "profile": {
                    "age": profile.age,
                    "gender": profile.gender,
                    "weight_kg": profile.weight,
                    "height_cm": profile.height,
                    "activity_level": profile.activity_level,
                    "goal": profile.goal,
                    "bmi": profile.bmi,
                    "bmi_category": profile.bmi_category,
                    "bmr_kcal": profile.bmr,
                    "tdee_baseline_kcal": profile.tdee_baseline
                },
                "plan": plan.to_dict()
            }
        }
        return jsonify(response), 200

    except ValidationError as ve:
        return jsonify({
            "success": False,
            "error": "Validation Error",
            "details": ve.errors()
        }), 422
    except Exception as e:
        current_app.logger.error(f"API prediction error: {e}", exc_info=True)
        return jsonify({"success": False, "error": str(e)}), 500

@api_bp.route('/metrics', methods=['GET'])
def metrics():
    """REST endpoint exposing ground-truth model performance metrics."""
    ml_service, _ = get_services()
    model_metrics = ml_service.get_metrics()
    return jsonify({
        "success": True,
        "metrics": model_metrics.model_dump()
    }), 200

@api_bp.route('/explain', methods=['POST'])
def explain():
    """Find top K most similar fitness profiles using k-NN metric distance."""
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 415

    ml_service, _ = get_services()
    if not ml_service.is_ready:
        return jsonify({"error": "ML Model is not loaded"}), 503

    try:
        data = request.get_json()
        profile = UserProfile(**data)
        k = int(request.args.get('k', 3))
        k = max(1, min(10, k))

        similar = ml_service.find_similar_profiles(profile.model_dump(), k=k)
        return jsonify({
            "success": True,
            "count": len(similar),
            "similar_profiles": [p.model_dump() for p in similar]
        }), 200
    except ValidationError as ve:
        return jsonify({"success": False, "error": "Validation Error", "details": ve.errors()}), 422
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
