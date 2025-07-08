import sqlite3
import pytest

from typing import Union
from src.macroquest_db import run_sql, insert_row

def util_load_file(path: str) -> str:
    with open(path, encoding='utf-8') as file:
        return file.read()

def test_validate_identifier_success():
    from src.macroquest_db import validate_identifier
    res = validate_identifier(identifier='test colomun')
    assert res


def test_validate_identifier_fail():
    from src.macroquest_db import validate_identifier
    res = validate_identifier(identifier='SELECT')
    assert res

@pytest.fixture
def in_memory_db(monkeypatch):
    """
    Fixture that creates an in-memory SQLite database and overrides `run_sql`
    to use this in-memory connection instead of disk-based DB.
    """
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE users (
            id TEXT PRIMARY KEY,
            name TEXT,
            age INTEGER
        )
    """)
    conn.commit()

    def test_run_sql(query: str, params: Union[tuple, list] = ()):
        cur = conn.cursor()
        cur.execute(query, params)
        conn.commit()

    monkeypatch.setattr("macroquest_db.run_sql", test_run_sql)  # Patch the real run_sql

    yield conn

    conn.close()


def test_run_sql_insert_and_select(in_memory_db):
    """
    Test `run_sql` by inserting a row and verifying it exists.
    """
    query = "INSERT INTO users (id, name, age) VALUES (?, ?, ?)"
    params = ("123", "Alice", 30)

    run_sql(query, params)

    result = in_memory_db.execute("SELECT * FROM users WHERE id = '123'").fetchone()
    assert result == ("123", "Alice", 30)


def test_insert_row_success(in_memory_db):
    """
    Test `insert_row` inserts a row with proper parameters.
    """
    data = {"id": "abc", "name": "Bob", "age": 25}
    insert_row("users", data)

    result = in_memory_db.execute("SELECT * FROM users WHERE id = 'abc'").fetchone()
    assert result == ("abc", "Bob", 25)


def test_insert_row_invalid_column_name(monkeypatch):
    """
    Test that insert_row raises a ValueError on invalid column name.
    """
    data = {"drop": "Evil", "name": "Inject", "age": 99}

    with pytest.raises(ValueError, match="Invalid table or column name."):
        insert_row("users", data)


def test_update_row():
    pass

def test_delete_row():
    pass