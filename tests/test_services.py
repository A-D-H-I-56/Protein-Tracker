import pytest
from app.models.user_profile import UserProfile
from app.services.meal_planner_service import MealPlannerService
from app.services.nutrition_service import NutritionService

class DummyMLService:
    def __init__(self):
        self.is_ready = True

    def predict(self, profile_dict):
        return {
            'calories': 2800,
            'protein': 140,
            'carbs': 350,
            'fat': 80
        }

    def find_similar_profiles(self, profile_dict, k=3):
        return []

def test_meal_planner_service():
    meals = MealPlannerService.generate_meal_breakdown(
        calories=2000,
        protein=160,
        carbs=200,
        fat=60,
        goal="Muscle Gain"
    )
    assert len(meals) == 4
    # Check total meal calories sum to approx 2000
    total_meal_cals = sum(m.calories for m in meals)
    assert abs(total_meal_cals - 2000) <= 5

    breakfast = meals[0]
    assert breakfast.name == "Breakfast"
    assert breakfast.percentage == 25
    assert len(breakfast.suggestions) > 0

def test_nutrition_service():
    dummy_ml = DummyMLService()
    nutrition_service = NutritionService(ml_service=dummy_ml)

    profile = UserProfile(
        age=25,
        gender="Male",
        weight=70.0,
        height=175.0,
        activity_level="Very Active",
        goal="Muscle Gain"
    )

    plan = nutrition_service.calculate_plan(profile)
    assert plan.calories == 2800
    assert plan.protein == 140
    assert plan.carbs == 350
    assert plan.fat == 80
    assert plan.tdee_baseline is not None
    assert plan.protein_per_kg == 2.0  # 140g / 70kg = 2.0
    assert len(plan.meals) == 4
