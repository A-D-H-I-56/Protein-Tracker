import os
from typing import Literal
from pydantic import BaseModel, Field, field_validator
from app.config import Config

class UserProfile(BaseModel):
    """
    Domain Entity and Validation Schema for User Biometric and Fitness Profile.
    Boundaries and limits are dynamically sourced from configuration / environment variables.
    """
    age: int = Field(..., ge=Config.MIN_AGE, le=Config.MAX_AGE, description="Age in years")
    gender: str = Field(..., description="Biological sex for metabolic baseline")
    weight: float = Field(..., ge=Config.MIN_WEIGHT, le=Config.MAX_WEIGHT, description="Body weight in kilograms")
    height: float = Field(..., ge=Config.MIN_HEIGHT, le=Config.MAX_HEIGHT, description="Body height in centimeters")
    activity_level: str = Field(..., description="Daily physical activity level")
    goal: str = Field(..., description="Primary fitness objective")

    @field_validator('gender')
    @classmethod
    def validate_gender(cls, v):
        if isinstance(v, str):
            v = v.strip().title()
        if v not in Config.ALLOWED_GENDERS:
            raise ValueError(f"Gender must be one of {Config.ALLOWED_GENDERS}, got '{v}'")
        return v

    @field_validator('activity_level')
    @classmethod
    def validate_activity_level(cls, v):
        if isinstance(v, str):
            v = v.strip().title()
        if v not in Config.ALLOWED_ACTIVITY_LEVELS:
            raise ValueError(f"Activity level must be one of {Config.ALLOWED_ACTIVITY_LEVELS}, got '{v}'")
        return v

    @field_validator('goal')
    @classmethod
    def validate_goal(cls, v):
        if isinstance(v, str):
            v = v.strip().title()
        if v not in Config.ALLOWED_GOALS:
            raise ValueError(f"Goal must be one of {Config.ALLOWED_GOALS}, got '{v}'")
        return v

    @property
    def bmi(self) -> float:
        """Calculate Body Mass Index (BMI = kg / m^2)."""
        height_m = self.height / 100.0
        return round(self.weight / (height_m ** 2), 1)

    @property
    def bmi_category(self) -> str:
        """Classify BMI into standard WHO categories."""
        bmi_val = self.bmi
        if bmi_val < 18.5:
            return "Underweight"
        elif bmi_val < 25.0:
            return "Normal weight"
        elif bmi_val < 30.0:
            return "Overweight"
        else:
            return "Obese"

    @property
    def bmr(self) -> float:
        """
        Calculate Basal Metabolic Rate (BMR) using the Mifflin-St Jeor Equation:
        Men: 10 * weight(kg) + 6.25 * height(cm) - 5 * age(y) + 5
        Women: 10 * weight(kg) + 6.25 * height(cm) - 5 * age(y) - 161
        """
        base = (10 * self.weight) + (6.25 * self.height) - (5 * self.age)
        return round(base + 5 if self.gender == 'Male' else base - 161, 1)

    @property
    def activity_multiplier(self) -> float:
        """Physical activity multipliers for TDEE estimation."""
        multipliers = {
            'Sedentary': 1.2,
            'Light Active': 1.375,
            'Active': 1.55,
            'Very Active': 1.725
        }
        return multipliers.get(self.activity_level, 1.2)

    @property
    def tdee_baseline(self) -> float:
        """Calculate Total Daily Energy Expenditure (TDEE) baseline."""
        return round(self.bmr * self.activity_multiplier, 0)
