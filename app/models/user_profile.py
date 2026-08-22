from typing import Literal
from pydantic import BaseModel, Field, field_validator

class UserProfile(BaseModel):
    """
    Domain Entity and Validation Schema for User Biometric and Fitness Profile.
    Strictly follows Single Responsibility Principle.
    """
    age: int = Field(..., ge=15, le=100, description="Age in years (15-100)")
    gender: Literal['Male', 'Female'] = Field(..., description="Biological sex for metabolic baseline")
    weight: float = Field(..., ge=40.0, le=200.0, description="Body weight in kilograms (40-200 kg)")
    height: float = Field(..., ge=140.0, le=220.0, description="Body height in centimeters (140-220 cm)")
    activity_level: Literal['Sedentary', 'Light Active', 'Active', 'Very Active'] = Field(
        ..., description="Daily physical activity level"
    )
    goal: Literal['Weight Loss', 'Maintenance', 'Muscle Gain'] = Field(
        ..., description="Primary fitness objective"
    )

    @field_validator('gender', mode='before')
    @classmethod
    def sanitize_gender(cls, v):
        if isinstance(v, str):
            v = v.strip().title()
        return v

    @field_validator('activity_level', mode='before')
    @classmethod
    def sanitize_activity_level(cls, v):
        if isinstance(v, str):
            v = v.strip().title()
        return v

    @field_validator('goal', mode='before')
    @classmethod
    def sanitize_goal(cls, v):
        if isinstance(v, str):
            v = v.strip().title()
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
