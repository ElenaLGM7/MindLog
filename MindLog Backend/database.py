import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("DATABASE_URL")

conn = psycopg2.connect(DB_URL, cursor_factory=RealDictCursor)
cursor = conn.cursor()

def create_tables():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS entries (
            id SERIAL PRIMARY KEY,
            text TEXT NOT NULL,
            emotions TEXT[],
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()

def save_entry(text: str, emotions: list[str], date: str):
    cursor.execute(
        "INSERT INTO entries (text, emotions, date) VALUES (%s, %s, %s);",
        (text, emotions, date)
    )
    conn.commit()
