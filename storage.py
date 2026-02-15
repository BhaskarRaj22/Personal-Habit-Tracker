import sqlite3
from contextlib import contextmanager
from typing import Any, Dict, List, Optional
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'assistant.db')

@contextmanager
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()

def init_db():
    with get_db() as conn:
        c = conn.cursor()
        # Tasks
        c.execute('''CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            priority TEXT,
            due_date TEXT,
            completed INTEGER DEFAULT 0,
            created_at TEXT,
            completed_at TEXT
        )''')
        # Habits
        c.execute('''CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            streak INTEGER DEFAULT 0,
            last_completed TEXT
        )''')
        # Habit Completions
        c.execute('''CREATE TABLE IF NOT EXISTS habit_completions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            habit_id INTEGER,
            date TEXT,
            FOREIGN KEY(habit_id) REFERENCES habits(id)
        )''')
        # Focus Sessions
        c.execute('''CREATE TABLE IF NOT EXISTS focus_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            start_time TEXT,
            end_time TEXT,
            duration INTEGER
        )''')

def fetch_all(query: str, params: tuple = ()) -> List[Dict[str, Any]]:
    with get_db() as conn:
        c = conn.cursor()
        c.execute(query, params)
        return [dict(row) for row in c.fetchall()]

def fetch_one(query: str, params: tuple = ()) -> Optional[Dict[str, Any]]:
    with get_db() as conn:
        c = conn.cursor()
        c.execute(query, params)
        row = c.fetchone()
        return dict(row) if row else None

def execute(query: str, params: tuple = ()) -> int:
    with get_db() as conn:
        c = conn.cursor()
        c.execute(query, params)
        return c.lastrowid
