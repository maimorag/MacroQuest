import sqlite3

import os
# Ensure the DB folder exists

os.makedirs("DB", exist_ok=True)
conn = sqlite3.connect("DB/macroquest.db")
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS foods (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE,
    calories REAL,
    protein REAL,
    carbs REAL,
    fat REAL,
    unit TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS meals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    food_id INTEGER,
    quantity REAL,
    FOREIGN KEY(food_id) REFERENCES foods(id)
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS daily_summary (
    date TEXT PRIMARY KEY,
    total_cal REAL,
    total_protein REAL,
    total_carbs REAL,
    total_fat REAL,
    goal_met INTEGER
)
""")

conn.commit()
conn.close()
