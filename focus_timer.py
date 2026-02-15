import time
from datetime import datetime, timedelta
from storage import execute
from rich.console import Console
from rich.progress import Progress, BarColumn, TimeRemainingColumn

class FocusTimer:
    def start_focus(self, minutes: int = 25, break_minutes: int = 5, cycles: int = 1):
        console = Console()
        for cycle in range(1, cycles + 1):
            console.print(f"[bold green]Focus Session {cycle} - {minutes} minutes[/bold green]")
            self._run_timer(minutes * 60, "Focus")
            start_time = datetime.now()
            end_time = start_time + timedelta(minutes=minutes)
            execute(
                "INSERT INTO focus_sessions (start_time, end_time, duration) VALUES (?, ?, ?)",
                (start_time.isoformat(), end_time.isoformat(), minutes)
            )
            if cycle < cycles:
                console.print(f"[bold blue]Break - {break_minutes} minutes[/bold blue]")
                self._run_timer(break_minutes * 60, "Break")
        console.print("[bold green]Focus session(s) complete![/bold green]")

    def _run_timer(self, seconds: int, label: str):
        with Progress(
            "{task.description}",
            BarColumn(),
            "[progress.percentage]{task.percentage:>3.0f}%",
            TimeRemainingColumn(),
        ) as progress:
            task = progress.add_task(f"{label} Timer", total=seconds)
            for _ in range(seconds):
                time.sleep(1)
                progress.update(task, advance=1)
