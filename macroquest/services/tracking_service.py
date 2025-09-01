from collections import defaultdict
from datetime import datetime

from macroquest.fdc_client.client import FoodDataCentralClient
from macroquest.fdc_client.recipe_calculator import RecipeCalculator
from macroquest.fdc_client.common import Nutrition, logger
from macroquest.db.db_manager import insert_meal, fetch_all_meals


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


def aggregate_daily_totals() -> dict[str, Nutrition]:
    """Aggregate all meals in the DB into daily totals."""
    rows = fetch_all_meals()
    if not rows:
        return {}

    totals: dict[str, Nutrition] = defaultdict(lambda: Nutrition())

    for name, grams, cal, protein, fat, carbs, ts in rows:
        # Extract just the date part (YYYY-MM-DD)
        date = datetime.fromisoformat(ts).date().isoformat()

        totals[date] = totals[date] + Nutrition(
            calories=cal,
            protein=protein,
            fat=fat,
            carbohydrates=carbs,
        )

    return dict(totals)
