from collections import defaultdict
from datetime import datetime

from macroquest.fdc_client.client import FoodDataCentralClient
from macroquest.fdc_client.recipe_calculator import RecipeCalculator
from macroquest.fdc_client.common import Nutrition, logger
from macroquest.db.db_manager import insert_meal, fetch_all_meals




def calc_nutritions(meals: dict[str, float], goals: Nutrition, skip_db: bool = False) -> dict[str, Nutrition]:
    """
    Calculate nutrition consumption compared to daily goals.

    Args:
        meals (dict[str, float]): Mapping of food items to gram amounts.
        goals (Nutrition): User's daily nutrition goals.
        skip_db (bool): If True, do not insert meals into the database.

    Returns:
        dict[str, Nutrition]: Consumed, remaining, and goal nutrition values.
    """
    client = FoodDataCentralClient()
    calculator = RecipeCalculator(client)

    consumed = calculator.get_recipe_nutrition(meals)

    if not skip_db:
        # Save each meal in DB only if lookup succeeds
        for name, grams in meals.items():
            try:
                single_nutrition = calculator.get_recipe_nutrition({name: grams})
                if (
                    single_nutrition is None
                    or single_nutrition.calories == 0
                    and single_nutrition.protein == 0
                    and single_nutrition.fat == 0
                    and single_nutrition.carbohydrates == 0
                ):
                    logger.warning(f"Skipping DB insert for '{name}' (no nutrition data).")
                    continue

                insert_meal(name, grams, single_nutrition)
            except Exception as e:
                logger.error(f"Skipping DB insert for '{name}' due to error: {e}")
                continue
    else:
        logger.info("Skipping DB inserts (--skip-db enabled).")

    left = Nutrition(
        calories=goals.calories - consumed.calories,
        protein=goals.protein - consumed.protein,
        fat=goals.fat - consumed.fat,
        carbohydrates=goals.carbohydrates - consumed.carbohydrates,
    )

    return {"consumed": consumed, "left": left, "goals": goals}



def export_excel(results: dict[str, Nutrition], path="nutrition_summary.xlsx"):
    """
    Export nutrition summary results into an Excel file.

    Args:
        results (dict[str, Nutrition]): Dictionary containing consumed, left, and goals.
        path (str): Output path for the Excel file.
    """
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
    """
    Aggregate all meals stored in the database into daily totals.

    Returns:
        dict[str, Nutrition]: Mapping from date (YYYY-MM-DD) to total nutrition.
    """
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
