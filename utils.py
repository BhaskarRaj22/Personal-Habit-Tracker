from datetime import datetime, date
from task_manager import TaskManager
from habit_tracker import HabitTracker
from storage import fetch_all

class Summary:
    def __init__(self):
        self.task_manager = TaskManager()
        self.habit_tracker = HabitTracker()

    def daily_summary(self):
        today = date.today().isoformat()
        completed_tasks = self.task_manager.get_completed_today()
        habits = self.habit_tracker.list_habits()
        habits_done = [h for h in habits if h['last_completed'] == today]
        focus_sessions = fetch_all(
            "SELECT * FROM focus_sessions WHERE date(start_time)=?",
            (today,)
        )
        summary = f"\n[bold underline]Daily Productivity Summary ({today})[/bold underline]\n"
        summary += f"\nTasks Completed: {len(completed_tasks)}"
        for t in completed_tasks:
            summary += f"\n  - {t['title']} (Priority: {t['priority']})"
        summary += f"\n\nHabits Tracked: {len(habits)}"
        for h in habits:
            streak = h['streak']
            done = '[x]' if h['last_completed'] == today else '[ ]'
            summary += f"\n  {done} {h['name']} (Streak: {streak})"
        summary += f"\n\nFocus Sessions: {len(focus_sessions)}"
        for f in focus_sessions:
            summary += f"\n  - {f['duration']} min ({f['start_time'][11:16]} - {f['end_time'][11:16]})"
        return summary
