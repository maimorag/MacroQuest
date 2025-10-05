import argparse
from pathlib import Path

from macroquest.services.tracking_service import (
    calc_nutritions,
    export_excel,
    aggregate_daily_totals,
)
from macroquest.utils.input_loader import load_goals, load_meals
from macroquest.db.db_manager import fetch_all_meals, fetch_meals_by_date


def parse_args():
    """
    Parse command-line arguments for meal tracking CLI.

    Returns:
        argparse.Namespace: Parsed arguments containing options like goals, meals,
        history, daily aggregation, and database skipping.
    """
    parser = argparse.ArgumentParser(
        description="Calculate consumed nutrition vs daily goals.",
        usage="meal_tracking.py [-h] [-g GOALS_PATH] [-m MEALS_PATH] [-e] [--history] [--daily]",
    )
    parser.add_argument(
        "-g", "--goals", type=Path, help="Path to goals JSON/Excel file."
    )
    parser.add_argument(
        "-m", "--meals", type=Path, help="Path to meals JSON/Excel file."
    )
    parser.add_argument(
        "-e", "--create-excel", action="store_true", help="Export results to Excel."
    )
    parser.add_argument(
        "--history", action="store_true", help="Show meal history from the database."
    )
    parser.add_argument(
        "--daily", action="store_true", help="Show daily aggregated nutrition totals."
    )
    parser.add_argument(
        "--date", type=str, help="Show meals only for a specific date (YYYY-MM-DD)."
    )
    parser.add_argument(
        "--skip-db",
        action="store_true",
        help="Skip saving meals into the local database.",
    )
    return parser.parse_args()


def show_history(daily: bool = False):
    """
    Display meal history or daily totals from the database.

    Args:
        daily (bool): If True, shows daily aggregated totals. Otherwise, shows
        raw meal history with timestamped entries.
    """
    if daily:
        totals = aggregate_daily_totals()
        if not totals:
            print("No daily totals found.")
            return

        print("\n=== Daily Nutrition Summary ===")
        for date, nutrition in totals.items():
            print(
                f"{date}: {nutrition.calories:.1f} kcal, "
                f"{nutrition.protein:.1f}P/{nutrition.fat:.1f}F/{nutrition.carbohydrates:.1f}C"
            )
    else:
        rows = fetch_all_meals()
        if not rows:
            print("No history found.")
            return

        print("\n=== Meal History ===")
        for name, grams, cal, protein, fat, carbs, ts in rows:
            print(
                f"[{ts}] {name} ({grams}g) -> "
                f"{cal:.1f} kcal, {protein:.1f}P/{fat:.1f}F/{carbs:.1f}C"
            )


def main():
    """
    Main entry point for the meal tracking CLI.

    Loads goals and meals, calculates nutrition summary, optionally exports
    results to Excel, and supports history/daily views.
    """
    args = parse_args()

    if args.history:
        show_history(daily=args.daily)
        return

    goals = load_goals(args.goals)
    meals = load_meals(args.meals)

    results = calc_nutritions(meals, goals, skip_db=args.skip_db)

    if args.create_excel:
        export_excel(results)
        if args.date:
            rows = fetch_meals_by_date(args.date)
            if not rows:
                print(f"No meals found for {args.date}.")
                return

            print(f"\n=== Meals for {args.date} ===")
            for name, grams, cal, protein, fat, carbs, ts in rows:
                print(
                    f"[{ts}] {name} ({grams}g) -> "
                    f"{cal:.1f} kcal, {protein:.1f}P/{fat:.1f}F/{carbs:.1f}C"
                )
            return

    print("\n=== Nutrition Summary ===")
    print("Consumed:")
    print(results["consumed"].model_dump_json(indent=2))
    print("Remaining:")
    print(results["left"].model_dump_json(indent=2))


if __name__ == "__main__":
    main()
