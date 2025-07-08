import sqlite3
import uuid
import os
from sqlite3 import IntegrityError, OperationalError
from typing import Union


def validate_identifier(identifier: str) -> bool:
    """
    Validates that a string is a safe SQL identifier 
    (table or column name).
    """
    return identifier.isidentifier() and identifier.lower() not in {"select", "drop", "delete", "update", "insert", "from"}



def init():
    os.makedirs("DB", exist_ok=True)
    conn = sqlite3.connect("DB/macroquest.db")
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS ingredients (
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
    CREATE TABLE IF NOT EXISTS foods (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        total_calories REAL,
        total_protein REAL,
        total_carbs REAL,
        total_fat REAL,
        unit TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS daily_meals (
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


def run_sql(query: str, params: Union[tuple, list] = ()):
    """
    Executes a given SQL query with optional parameterized values.

    Parameters:
        query (str): The SQL query to execute (may include placeholders `?`).
        params (tuple | list): Values to substitute into the query securely.
    Raises:
        RuntimeError: If an SQL error occurs.
    """
    try:
        conn = sqlite3.connect("DB/macroquest.db")
        c = conn.cursor()
        c.execute(query, params)
        conn.commit()
    except IntegrityError as e:
        raise RuntimeError(f"Integrity error while executing SQL: {e}")
    except OperationalError as e:
        raise RuntimeError(f"SQL operation failed: {e}")
    finally:
        conn.close()


def insert_row(table: str, data: dict[str, str]):
    """
    Inserts a new row into the specified table with the given column-value pairs.

    Parameters:
        table (str): Name of the table.
        data (dict[str, str]): Dictionary mapping column names to their values.

    Notes:
        - Values are parameterized safely.
        - Table and column names must be valid identifiers.
    """
    if not validate_identifier(table) or not all(validate_identifier(k) for k in data):
        raise ValueError("Invalid table or column name.")

    columns = ', '.join(data.keys())
    placeholders = ', '.join(['?'] * len(data))
    values = list(data.values())

    query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
    run_sql(query, values)


def update_row(table: str, key_column: str, key_value: str, updates: dict[str, str]):
    """
    Updates a row in the specified table using a key match and new values.

    Parameters:
        table (str): Name of the table.
        key_column (str): Column to match the row by.
        key_value (str): Value to match in the key column.
        updates (dict[str, str]): Column-value pairs to update.

    Notes:
        - Parameterized to prevent SQL injection.
        - Validates table and column names.
    """
    if not (validate_identifier(table) and validate_identifier(key_column)) or not all(validate_identifier(k) for k in updates):
        raise ValueError("Invalid table or column name.")

    set_clause = ', '.join(f"{col} = ?" for col in updates)
    values = list(updates.values()) + [key_value]

    query = f"UPDATE {table} SET {set_clause} WHERE {key_column} = ?"
    run_sql(query, values)


def delete_row(table: str, key_column: str, key_value: str):
    """
    Deletes a row from the specified table based on a key match.

    Parameters:
        table (str): Name of the table.
        key_column (str): Column to match the row by.
        key_value (str): Value to match.

    Raises:
        ValueError: If identifier is not safe.
    """
    if not (validate_identifier(table) and validate_identifier(key_column)):
        raise ValueError("Invalid table or column name.")

    query = f"DELETE FROM {table} WHERE {key_column} = ?"
    run_sql(query, (key_value,))


def log_meal(food_name: str, quantity: float, meal_date: str = None):
    """
    Logs a meal eaten by inserting a record into the `daily_meals` table.

    Parameters:
        food_name (str): Name of the food (must exist in `foods` table).
        quantity (float): How much was eaten (same unit as defined in `foods.unit`).
        meal_date (str, optional): Date in YYYY-MM-DD format. Defaults to today.

    Raises:
        ValueError: If the food name is not found in the `foods` table.
    """
    meal_date = meal_date or date.today().isoformat()

    # Step 1: Get the food_id
    query = "SELECT id FROM foods WHERE name = ?"
    conn = sqlite3.connect("DB/macroquest.db")
    cur = conn.cursor()
    cur.execute(query, (food_name,))
    result = cur.fetchone()
    conn.close()

    if not result:
        raise ValueError(f"Food '{food_name}' not found in database.")
    
    food_id = result[0]

    # Step 2: Insert the meal record
    row_data = {
        "date": meal_date,
        "food_id": food_id,
        "quantity": quantity
    }
    insert_row("daily_meals", row_data)

def main():
    init()


# Using the special variable 
# __name__
if __name__=="__main__":
    main()