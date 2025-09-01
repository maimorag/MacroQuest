import logging
import os
from typing import List, Dict, Optional, Any
from pydantic import BaseModel
from datetime import datetime

# -------- Global Constants -------- #
BASE_URL = "https://api.nal.usda.gov/fdc"
API_KEY_REQUEST_URL = "https://nal.altarama.com/reft100.aspx?key=FoodData"
DEFAULT_CONFIG_FILE = os.path.join(os.getcwd(), "config_fdc.json")

# -------- Global Logger -------- #
logger = logging.getLogger("FoodDataCentral")
logger.setLevel(logging.INFO)

_handler = logging.StreamHandler()
_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
_handler.setFormatter(_formatter)
logger.addHandler(_handler)

# -------- Data Models -------- #
class Nutrition(BaseModel):
    calories: float = 0.0
    protein: float = 0.0
    fat: float = 0.0
    carbohydrates: float = 0.0

    def __add__(self, other: "Nutrition") -> "Nutrition":
        return Nutrition(
            calories=self.calories + other.calories,
            protein=self.protein + other.protein,
            fat=self.fat + other.fat,
            carbohydrates=self.carbohydrates + other.carbohydrates,
        )

    def scale(self, factor: float) -> "Nutrition":
        return Nutrition(
            calories=self.calories * factor,
            protein=self.protein * factor,
            fat=self.fat * factor,
            carbohydrates=self.carbohydrates * factor,
        )

class Meal(BaseModel):
    name: str
    grams: float
    nutrition: Nutrition
    timestamp: datetime

__all__ = [
    "BASE_URL",
    "API_KEY_REQUEST_URL",
    "DEFAULT_CONFIG_FILE",
    "logger",
    "List",
    "Dict",
    "Optional",
    "Any",
    "Nutrition",
    "Meal",
]
