import json
from pathlib import Path
from macroquest.fdc_client.common import Nutrition, logger


def read_json(path: Path):
    """
    Read a JSON file and return its contents.

    Args:
        path (Path): Path to the JSON file.

    Returns:
        dict: Parsed JSON data.
    """
    try:
        with open(path, "r") as file:
            data = json.load(file)
            logger.info(f"Loaded JSON from {path}")
            return data
    except Exception as e:
        logger.error(f"Failed to read JSON {path}: {e}")
        return {}


def read_excel(path: Path):
    """
    Load daily nutrition goals from a JSON/Excel file or prompt interactively.

    Args:
        path (Path | None): Path to file, or None for interactive mode.

    Returns:
        Nutrition: Daily nutrition goals.
    """
    try:
        import openpyxl

        wb = openpyxl.load_workbook(path)
        ws = wb.active
        data = {}
        for row in ws.iter_rows(min_row=2, values_only=True):
            if row[0] and row[1]:
                data[str(row[0])] = float(row[1])
        logger.info(f"Loaded Excel from {path}")
        return data
    except Exception as e:
        logger.error(f"Failed to read Excel {path}: {e}")
        return {}


def ask_interactive_goals() -> Nutrition:
    print("Enter your daily nutrition goals:")
    return Nutrition(
        calories=float(input("Calories: ")),
        protein=float(input("Protein (g): ")),
        fat=float(input("Fat (g): ")),
        carbohydrates=float(input("Carbohydrates (g): ")),
    )


def ask_interactive_meals() -> dict[str, float]:
    print("Enter meals (food name + grams). Type 'done' to finish.")
    meals = {}
    while True:
        food = input("Food name (or 'done'): ").strip()
        if food.lower() == "done":
            break
        try:
            grams = float(input(f"Grams of {food}: "))
            meals[food] = grams
        except ValueError:
            print("Invalid number, try again.")
    return meals


def load_goals(path: Path | None) -> Nutrition:
    if not path:
        return ask_interactive_goals()
    if path.suffix.lower() == ".json":
        return Nutrition(**read_json(path))
    elif path.suffix.lower() in [".xls", ".xlsx"]:
        return Nutrition(**read_excel(path))
    else:
        logger.error("Unsupported goals file format")
        return ask_interactive_goals()


def load_meals(path: Path | None) -> dict[str, float]:
    if not path:
        return ask_interactive_meals()
    if path.suffix.lower() == ".json":
        return read_json(path)
    elif path.suffix.lower() in [".xls", ".xlsx"]:
        return read_excel(path)
    else:
        logger.error("Unsupported meals file format")
        return ask_interactive_meals()
