from macroquest.fdc_client.client import FoodDataCentralClient
from macroquest.fdc_client.common import Nutrition, logger



class RecipeCalculator:
    def __init__(self, client: FoodDataCentralClient):
        self.client = client

    def get_recipe_nutrition(self, ingredients: Dict[str, float], servings: int = 1) -> Nutrition:
        total = Nutrition()

        for ingredient, grams in ingredients.items():
            try:
                result = self.client.search_foods(ingredient, page_size=1)
                if not result.get("foods"):
                    logger.warning(f"No results found for {ingredient}")
                    continue

                food_id = result["foods"][0]["fdcId"]
                details = self.client.get_food(food_id)
                nutrition = self.client.extract_nutrition(details)

                serving_size = details.get("servingSize")
                serving_unit = details.get("servingSizeUnit", "").lower()
                factor = grams / float(serving_size) if serving_size and serving_unit == "g" else grams / 100.0

                total = total + nutrition.scale(factor)

            except Exception as e:
                logger.error(f"Error processing {ingredient}: {e}")

        return total.scale(1 / servings) if servings > 1 else total
