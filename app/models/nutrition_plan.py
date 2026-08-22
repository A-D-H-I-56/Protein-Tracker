from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class MealItem(BaseModel):
    name: str
    portion: str
    calories: int
    protein: int
    carbs: int
    fat: int

class MealCategory(BaseModel):
    name: str
    percentage: int
    calories: int
    protein: int
    carbs: int
    fat: int
    suggestions: List[str]

class SimilarProfile(BaseModel):
    similarity_score: float
    age: int
    gender: str
    weight: float
    height: float
    activity_level: str
    goal: str
    calories: int
    protein: int
    carbs: int
    fat: int

class NutritionPlan(BaseModel):
    """
    Domain Entity representing the tailored nutrition recommendation output.
    """
    calories: int = Field(..., ge=800, le=6000, description="Daily target calories in kcal")
    protein: int = Field(..., ge=30, le=400, description="Daily target protein in grams")
    carbs: int = Field(..., ge=20, le=800, description="Daily target carbohydrates in grams")
    fat: int = Field(..., ge=15, le=300, description="Daily target fat in grams")
    
    # Metadata & Insights
    tdee_baseline: Optional[float] = None
    calorie_delta: Optional[int] = None  # Delta vs TDEE (+ for surplus, - for deficit)
    protein_per_kg: Optional[float] = None
    
    # Explainable AI / Nearest Neighbors
    similar_profiles: List[SimilarProfile] = []
    
    # Meal Breakdown
    meals: List[MealCategory] = []

    @property
    def protein_calories(self) -> int:
        return self.protein * 4

    @property
    def carbs_calories(self) -> int:
        return self.carbs * 4

    @property
    def fat_calories(self) -> int:
        return self.fat * 9

    @property
    def calculated_total_calories(self) -> int:
        return self.protein_calories + self.carbs_calories + self.fat_calories

    @property
    def protein_ratio(self) -> int:
        return round((self.protein_calories / self.calories * 100)) if self.calories > 0 else 0

    @property
    def carbs_ratio(self) -> int:
        return round((self.carbs_calories / self.calories * 100)) if self.calories > 0 else 0

    @property
    def fat_ratio(self) -> int:
        return round((self.fat_calories / self.calories * 100)) if self.calories > 0 else 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            'calories': self.calories,
            'protein': self.protein,
            'carbs': self.carbs,
            'fat': self.fat,
            'protein_calories': self.protein_calories,
            'carbs_calories': self.carbs_calories,
            'fat_calories': self.fat_calories,
            'protein_ratio': self.protein_ratio,
            'carbs_ratio': self.carbs_ratio,
            'fat_ratio': self.fat_ratio,
            'tdee_baseline': self.tdee_baseline,
            'calorie_delta': self.calorie_delta,
            'protein_per_kg': self.protein_per_kg,
            'similar_profiles': [p.model_dump() for p in self.similar_profiles],
            'meals': [m.model_dump() for m in self.meals]
        }
