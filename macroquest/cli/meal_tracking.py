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
    parser = argparse.ArgumentParser(
        description="Calculate consumed nutrition vs daily goals.",
        usage="meal_tracking.py [-h] [-g GOALS_PATH] [-m MEALS_PATH] [-e] [--history] [--daily]",
    )
    parser.add_argument("-g", "--goals", type=Path, help="Path to goals JSON/Excel file.")
    parser.add_argument("-m", "--meals", type=Path, help="Path to meals JSON/Excel file.")
    parser.add_argument("-e", "--create-excel", action="store_true", help="Export results to Excel.")
    parser.add_argument("--history", action="store_true", help="Show meal history from the database.")
    parser.add_argument("--daily", action="store_true", help="Show daily aggregated nutrition totals.")
    parser.add_argument("--date", type=str, help="Show meals only for a specific date (YYYY-MM-DD).")
    return parser.parse_args()


def show_history(daily: bool = False):
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
    args = parse_args()

    if args.history:
        show_history(daily=args.daily)
        return
    
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

    goals = load_goals(args.goals)
    meals = load_meals(args.meals)

    results = calc_nutritions(meals, goals)

    print("\n=== Nutrition Summary ===")
    print("Consumed:")
    print(results["consumed"].json(indent=2))
    print("Remaining:")
    print(results["left"].json(indent=2))
    

    


if __name__ == "__main__":
    main()
