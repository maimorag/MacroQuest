import requests
import json
import os
import webbrowser

from .common import (
    BASE_URL,
    API_KEY_REQUEST_URL,
    DEFAULT_CONFIG_FILE,
    logger,
    List,
    Dict,
    Optional,
    Any,
    Nutrition,
)


class FoodDataCentralClient:
    def __init__(
        self, api_key: Optional[str] = None, config_path: Optional[str] = None
    ):
        self.config_path = config_path or DEFAULT_CONFIG_FILE

        if api_key:
            self.api_key = api_key
            logger.info("Initialized with API key provided directly.")
        else:
            self.api_key = self._load_api_key()
            if self.api_key:
                logger.info(f"Initialized with API key from {self.config_path}.")
            else:
                logger.warning(
                    "No API key found. Use create_api_key() and save_api_key()."
                )

    def _load_api_key(self) -> Optional[str]:
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r") as f:
                    data = json.load(f)
                return data.get("api_key")
            except Exception as e:
                logger.error(f"Failed to load API key from {self.config_path}: {e}")
        return None

    def save_api_key(self, api_key: str):
        try:
            with open(self.config_path, "w") as f:
                json.dump({"api_key": api_key}, f)
            self.api_key = api_key
            logger.info(f"API key saved to {self.config_path}")
        except Exception as e:
            logger.error(f"Failed to save API key: {e}")

    @classmethod
    def create_api_key(cls, open_browser: bool = True) -> str:
        logger.info("To obtain an API key, submit the USDA request form.")
        logger.info(f"Form URL: {API_KEY_REQUEST_URL}")
        if open_browser:
            try:
                webbrowser.open(API_KEY_REQUEST_URL)
                logger.info("Opened browser to API key request form.")
            except Exception as e:
                logger.error(f"Could not open browser: {e}")
        return API_KEY_REQUEST_URL

    def _get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Any:
        if not self.api_key:
            raise ValueError("API key missing.")
        params = params or {}
        params["api_key"] = self.api_key
        url = f"{BASE_URL}{endpoint}"
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def _post(self, endpoint: str, body: Dict[str, Any]) -> Any:
        if not self.api_key:
            raise ValueError("API key missing.")
        url = f"{BASE_URL}{endpoint}?api_key={self.api_key}"
        response = requests.post(url, json=body)
        response.raise_for_status()
        return response.json()

    def get_food(
        self, fdc_id: str, format: str = "full", nutrients: Optional[List[int]] = None
    ) -> Dict[str, Any]:
        params = {"format": format}
        if nutrients:
            params["nutrients"] = ",".join(map(str, nutrients))
        return self._get(f"/v1/food/{fdc_id}", params)

    def search_foods(
        self, query: str, page_size: int = 50, page_number: int = 1
    ) -> Dict[str, Any]:
        params = {"query": query, "pageSize": page_size, "pageNumber": page_number}
        return self._get("/v1/foods/search", params)

    def extract_nutrition(self, food_data: Dict[str, Any]) -> Nutrition:
        """
        Extract calories, protein, fat, carbohydrates (per serving or per 100g).
        """
        nutrients = Nutrition()

        if "labelNutrients" in food_data:  # Branded
            ln = food_data["labelNutrients"]
            nutrients = Nutrition(
                calories=ln.get("calories", {}).get("value", 0.0),
                protein=ln.get("protein", {}).get("value", 0.0),
                fat=ln.get("fat", {}).get("value", 0.0),
                carbohydrates=ln.get("carbohydrates", {}).get("value", 0.0),
            )
        elif "foodNutrients" in food_data:  # Foundation / SR Legacy
            for n in food_data["foodNutrients"]:
                name = n.get("nutrient", {}).get("name", "").lower()
                amount = n.get("amount")
                if not amount:
                    continue
                if "energy" in name or "calories" in name:
                    nutrients.calories = amount
                elif "protein" in name:
                    nutrients.protein = amount
                elif name.startswith("total lipid") or "fat" in name:
                    nutrients.fat = amount
                elif "carbohydrate" in name:
                    nutrients.carbohydrates = amount
        return nutrients
