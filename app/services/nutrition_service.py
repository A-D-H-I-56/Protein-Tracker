from typing import Dict, Any
from app.models.user_profile import UserProfile
from app.models.nutrition_plan import NutritionPlan
from app.services.meal_planner_service import MealPlannerService

class NutritionService:
    """
    Business Logic Service for processing Nutrition Analytics,
    calculating metabolic baselines, deltas, and creating unified NutritionPlan instances.
    """
    def __init__(self, ml_service):
        self.ml_service = ml_service

    def calculate_plan(self, profile: UserProfile) -> NutritionPlan:
        """
        Calculates complete personalized nutrition recommendation:
        1. Queries ML Engine for regression predictions.
        2. Computes baseline TDEE and BMR comparison metrics.
        3. Generates 4-stage meal breakdown.
        4. Queries XAI for nearest neighbor profiles.
        """
        profile_dict = profile.model_dump()

        # Step 1: Run ML prediction
        prediction = self.ml_service.predict(profile_dict)
        calories = prediction['calories']
        protein = prediction['protein']
        carbs = prediction['carbs']
        fat = prediction['fat']

        # Step 2: Compute scientific baseline metrics
        tdee_baseline = profile.tdee_baseline
        calorie_delta = int(round(calories - tdee_baseline))
        protein_per_kg = round(protein / profile.weight, 2)

        # Step 3: Meal planning breakdown
        meals = MealPlannerService.generate_meal_breakdown(
            calories=calories,
            protein=protein,
            carbs=carbs,
            fat=fat,
            goal=profile.goal
        )

        # Step 4: Nearest neighbors (Explainability)
        similar_profiles = self.ml_service.find_similar_profiles(profile_dict, k=3)

        return NutritionPlan(
            calories=calories,
            protein=protein,
            carbs=carbs,
            fat=fat,
            tdee_baseline=tdee_baseline,
            calorie_delta=calorie_delta,
            protein_per_kg=protein_per_kg,
            similar_profiles=similar_profiles,
            meals=meals
        )
