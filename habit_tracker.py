from typing import List, Dict, Optional
from datetime import datetime, date, timedelta
from storage import fetch_all, fetch_one, execute

class HabitTracker:
    def add_habit(self, name: str) -> int:
        return execute("INSERT INTO habits (name, streak, last_completed) VALUES (?, 0, NULL)", (name,))

    def list_habits(self) -> List[Dict]:
        return fetch_all("SELECT * FROM habits ORDER BY id")

    def mark_habit(self, habit_id: int) -> bool:
        today = date.today().isoformat()
        habit = fetch_one("SELECT * FROM habits WHERE id=?", (habit_id,))
        if not habit:
            return False
        last_completed = habit['last_completed']
        streak = habit['streak']
        if last_completed == today:
            return False  # Already marked today
        if last_completed == (date.today() - timedelta(days=1)).isoformat():
            streak += 1
        else:
            streak = 1
        execute("INSERT INTO habit_completions (habit_id, date) VALUES (?, ?)", (habit_id, today))
        return execute("UPDATE habits SET streak=?, last_completed=? WHERE id=?", (streak, today, habit_id)) > 0

    def get_streak(self, habit_id: int) -> Optional[int]:
        habit = fetch_one("SELECT * FROM habits WHERE id=?", (habit_id,))
        return habit['streak'] if habit else None

    def get_habit(self, habit_id: int) -> Optional[Dict]:
        return fetch_one("SELECT * FROM habits WHERE id=?", (habit_id,))

    def get_habit_completions(self, habit_id: int) -> List[Dict]:
        return fetch_all("SELECT * FROM habit_completions WHERE habit_id=? ORDER BY date DESC", (habit_id,))
