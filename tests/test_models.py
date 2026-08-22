import pytest
from pydantic import ValidationError
from app.models.user_profile import UserProfile
from app.models.nutrition_plan import NutritionPlan, MealCategory, SimilarProfile

def test_user_profile_valid():
    profile = UserProfile(
        age=25,
        gender="Male",
        weight=70.0,
        height=175.0,
        activity_level="Very Active",
        goal="Muscle Gain"
    )
    assert profile.age == 25
    assert profile.gender == "Male"
    assert profile.weight == 70.0
    assert profile.height == 175.0
    assert profile.activity_level == "Very Active"
    assert profile.goal == "Muscle Gain"

    # Computed metrics
    assert profile.bmi == 22.9
    assert profile.bmi_category == "Normal weight"
    assert profile.bmr == 1673.8
    assert profile.activity_multiplier == 1.725
    assert profile.tdee_baseline > 2000

def test_user_profile_sanitization():
    # Lowercase inputs should be auto-capitalized by validator
    profile = UserProfile(
        age=30,
        gender="female",
        weight=65.0,
        height=165.0,
        activity_level="light active",
        goal="weight loss"
    )
    assert profile.gender == "Female"
    assert profile.activity_level == "Light Active"
    assert profile.goal == "Weight Loss"

def test_user_profile_invalid_age():
    with pytest.raises(ValidationError):
        UserProfile(
            age=10, # Below 15
            gender="Male",
            weight=70.0,
            height=175.0,
            activity_level="Active",
            goal="Maintenance"
        )

def test_user_profile_invalid_weight():
    with pytest.raises(ValidationError):
        UserProfile(
            age=25,
            gender="Male",
            weight=300.0, # Above 200kg
            height=175.0,
            activity_level="Active",
            goal="Maintenance"
        )

def test_nutrition_plan_macro_ratios():
    plan = NutritionPlan(
        calories=2000,
        protein=150,
        carbs=200,
        fat=67
    )
    # Protein: 150*4 = 600 kcal (30%)
    # Carbs: 200*4 = 800 kcal (40%)
    # Fat: 67*9 = 603 kcal (30%)
    assert plan.protein_calories == 600
    assert plan.carbs_calories == 800
    assert plan.fat_calories == 603
    assert plan.protein_ratio == 30
    assert plan.carbs_ratio == 40
    assert plan.fat_ratio == 30
