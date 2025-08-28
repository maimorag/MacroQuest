import sqlite3
from pathlib import Path
from datetime import datetime
from fdc_client.common import logger, Nutrition


DB_PATH = Path(__file__).resolve().parent / "macroquest.db"


def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS meals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            grams REAL NOT NULL,
            calories REAL,
            protein REAL,
            fat REAL,
            carbohydrates REAL,
            timestamp TEXT NOT NULL
        )
        """)
        conn.commit()


def insert_meal(name: str, grams: float, nutrition: Nutrition):
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("""
        INSERT INTO meals (name, grams, calories, protein, fat, carbohydrates, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            name,
            grams,
            nutrition.calories,
            nutrition.protein,
            nutrition.fat,
            nutrition.carbohydrates,
            datetime.utcnow().isoformat()
        ))
        conn.commit()
        logger.info(f"Meal '{name}' inserted into DB.")


def fetch_all_meals():
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM meals ORDER BY timestamp DESC")
        return cur.fetchall()
