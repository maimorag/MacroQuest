from fdc_client.client import FoodDataCentralClient
from fdc_client.recipe_calculator import RecipeCalculator
from fdc_client.common import Nutrition, logger
from db.db_manager import insert_meal


def calc_nutritions(meals: dict[str, float], goals: Nutrition) -> dict[str, Nutrition]:
    client = FoodDataCentralClient()
    calculator = RecipeCalculator(client)

    consumed = calculator.get_recipe_nutrition(meals)

    # Save each meal in DB
    for name, grams in meals.items():
        insert_meal(name, grams, calculator.get_recipe_nutrition({name: grams}))

    left = Nutrition(
        calories=goals.calories - consumed.calories,
        protein=goals.protein - consumed.protein,
        fat=goals.fat - consumed.fat,
        carbohydrates=goals.carbohydrates - consumed.carbohydrates,
    )

    return {"consumed": consumed, "left": left, "goals": goals}


def export_excel(results: dict[str, Nutrition], path="nutrition_summary.xlsx"):
    try:
        import openpyxl
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Nutrition Summary"

        ws.append(["Metric", "Consumed", "Left", "Goal"])
        for metric in ["calories", "protein", "fat", "carbohydrates"]:
            ws.append([
                metric.capitalize(),
                getattr(results["consumed"], metric),
                getattr(results["left"], metric),
                getattr(results["goals"], metric),
            ])

        wb.save(path)
        logger.info(f"Excel file saved at {path}")
    except Exception as e:
        logger.error(f"Failed to create Excel file: {e}")
