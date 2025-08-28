import argparse
from pathlib import Path
from fdc_client.common import logger, Nutrition
from services.tracking_service import calc_nutritions, export_excel
from utils.input_loader import load_goals, load_meals   # put the load+interactive funcs here


def parse_args():
    parser = argparse.ArgumentParser(
        description="Calculate consumed nutrition vs daily goals.",
        usage="meal_tracking.py [-h] [-g GOALS_PATH] [-m MEALS_PATH] [-e]"
    )
    parser.add_argument("-g", "--goals", type=Path, help="Path to goals JSON/Excel file.")
    parser.add_argument("-m", "--meals", type=Path, help="Path to meals JSON/Excel file.")
    parser.add_argument("-e", "--create-excel", action="store_true", help="Export results to Excel.")
    return parser.parse_args()


def main():
    args = parse_args()
    goals = load_goals(args.goals)
    meals = load_meals(args.meals)

    results = calc_nutritions(meals, goals)

    print("\n=== Nutrition Summary ===")
    print("Consumed:")
    print(results["consumed"].json(indent=2))
    print("Remaining:")
    print(results["left"].json(indent=2))

    if args.create_excel:
        export_excel(results)


if __name__ == "__main__":
    main()
