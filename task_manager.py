from typing import List, Optional, Dict
from datetime import datetime
from storage import fetch_all, fetch_one, execute

class TaskManager:
    PRIORITIES = ['low', 'medium', 'high']

    def add_task(self, title: str, priority: str = 'medium', due_date: Optional[str] = None) -> int:
        if priority not in self.PRIORITIES:
            raise ValueError(f"Priority must be one of {self.PRIORITIES}")
        created_at = datetime.now().isoformat()
        return execute(
            "INSERT INTO tasks (title, priority, due_date, created_at) VALUES (?, ?, ?, ?)",
            (title, priority, due_date, created_at)
        )

    def list_tasks(self, show_all: bool = False) -> List[Dict]:
        if show_all:
            return fetch_all("SELECT * FROM tasks ORDER BY completed, due_date IS NULL, due_date, priority DESC, id")
        return fetch_all("SELECT * FROM tasks WHERE completed=0 ORDER BY due_date IS NULL, due_date, priority DESC, id")

    def complete_task(self, task_id: int) -> bool:
        completed_at = datetime.now().isoformat()
        return execute(
            "UPDATE tasks SET completed=1, completed_at=? WHERE id=?",
            (completed_at, task_id)
        ) > 0

    def delete_task(self, task_id: int) -> bool:
        return execute("DELETE FROM tasks WHERE id=?", (task_id,)) > 0

    def update_task(self, task_id: int, title: Optional[str] = None, priority: Optional[str] = None, due_date: Optional[str] = None) -> bool:
        task = fetch_one("SELECT * FROM tasks WHERE id=?", (task_id,))
        if not task:
            return False
        new_title = title if title else task['title']
        new_priority = priority if priority else task['priority']
        new_due = due_date if due_date else task['due_date']
        return execute(
            "UPDATE tasks SET title=?, priority=?, due_date=? WHERE id=?",
            (new_title, new_priority, new_due, task_id)
        ) > 0

    def get_task(self, task_id: int) -> Optional[Dict]:
        return fetch_one("SELECT * FROM tasks WHERE id=?", (task_id,))

    def get_completed_today(self) -> List[Dict]:
        today = datetime.now().date().isoformat()
        return fetch_all(
            "SELECT * FROM tasks WHERE completed=1 AND date(completed_at)=?",
            (today,)
        )
