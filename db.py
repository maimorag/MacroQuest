import sqlite3 as sql

DB_PATH = 'macro_logger.db'

con = sql.connect(DB_PATH)
cur = con.cursor()
cur.execute('''
            CREATE TABLE IF NOT EXISTS nutritions_100g
            (food_name text PRIMARY KEY, calories number, protein number,fat number, carbs number)
            ''')

cur.execute('''INSERT OR IGNORE INTO nutritions_100g VALUES ('cooked_rice','130','2.7','0.3', '28')''')

con.commit()