import sqlite3
from datetime import datetime
from pathlib import Path

from macroquest.fdc_client.common import logger, Nutrition

DB_PATH = Path(__file__).resolve().parent / "macroquest.db"


def init_db():
    """Initialize the meals table if it does not exist."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS meals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                grams REAL NOT NULL,
                calories REAL NOT NULL,
                protein REAL NOT NULL,
                fat REAL NOT NULL,
                carbs REAL NOT NULL,
                timestamp TEXT NOT NULL
            )
            """
        )
        conn.commit()


def insert_meal(name: str, grams: float, nutrition: Nutrition) -> None:
    """Insert a meal into the database with a timestamp."""
    try:
        ts = datetime.now().isoformat(timespec="seconds")
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO meals (name, grams, calories, protein, fat, carbs, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    name,
                    grams,
                    nutrition.calories,
                    nutrition.protein,
                    nutrition.fat,
                    nutrition.carbohydrates,
                    ts,
                ),
            )
            conn.commit()
            logger.info(f"Meal '{name}' inserted successfully at {ts}")
    except Exception as e:
        logger.error(f"Error inserting meal: {e}")


def fetch_all_meals():
    """Fetch all meals from the database."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT name, grams, calories, protein, fat, carbs, timestamp
                FROM meals
                ORDER BY timestamp ASC
                """
            )
            rows = cursor.fetchall()
        return rows
    except Exception as e:
        logger.error(f"Error fetching meals: {e}")
        return []


def fetch_meals_by_date(date: str):
    """
    Fetch meals for a specific date (YYYY-MM-DD).
    Example: fetch_meals_by_date("2025-09-01")
    """
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT name, grams, calories, protein, fat, carbs, timestamp
                FROM meals
                WHERE DATE(timestamp) = ?
                ORDER BY timestamp ASC
                """,
                (date,),
            )
            rows = cursor.fetchall()
        return rows
    except Exception as e:
        logger.error(f"Error fetching meals for {date}: {e}")
        return []


# Ensure the table exists at import
init_db()
