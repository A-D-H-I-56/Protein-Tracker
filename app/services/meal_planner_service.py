from typing import List
from app.models.nutrition_plan import MealCategory

class MealPlannerService:
    """
    Business Logic Service for generating targeted meal breakdowns and food suggestions.
    Follows Single Responsibility Principle.
    """
    @staticmethod
    def generate_meal_breakdown(calories: int, protein: int, carbs: int, fat: int, goal: str) -> List[MealCategory]:
        """
        Divides daily nutrition targets into 4 structured meals:
        - Breakfast: 25%
        - Lunch: 35%
        - Dinner: 25%
        - Snacks & Workout Fuel: 15%
        """
        distribution = [
            {
                "name": "Breakfast",
                "pct": 0.25,
                "suggestions": [
                    "Eggs/Egg Whites with whole-grain oats & berries",
                    "Greek yogurt parfait with chia seeds & almond butter",
                    "High-protein smoothie with whey, spinach & banana"
                ]
            },
            {
                "name": "Lunch",
                "pct": 0.35,
                "suggestions": [
                    "Grilled chicken breast with brown rice & broccoli",
                    "Salmon fillet with sweet potato & asparagus",
                    "Tofu/Tempeh quinoa bowl with mixed vegetables & olive oil"
                ]
            },
            {
                "name": "Dinner",
                "pct": 0.25,
                "suggestions": [
                    "Lean beef or turkey stir-fry with zucchini & bell peppers",
                    "White fish / Cod with roasted baby potatoes & greens",
                    "Lentil and chickpea curry with spinach salad"
                ]
            },
            {
                "name": "Snacks & Pre/Post Workout",
                "pct": 0.15,
                "suggestions": [
                    "Cottage cheese with walnuts or rice cakes",
                    "Protein shake with an apple or rice cakes",
                    "Hard-boiled eggs and a handful of almonds"
                ]
            }
        ]

        meals = []
        for meal in distribution:
            pct = meal["pct"]
            meals.append(MealCategory(
                name=meal["name"],
                percentage=int(pct * 100),
                calories=int(round(calories * pct)),
                protein=int(round(protein * pct)),
                carbs=int(round(carbs * pct)),
                fat=int(round(fat * pct)),
                suggestions=meal["suggestions"]
            ))

        return meals
