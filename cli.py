from task_manager import TaskManager
from habit_tracker import HabitTracker
from focus_timer import FocusTimer
from utils import Summary
from storage import init_db
from rich.console import Console
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from dateutil.parser import parse as parse_date

COMMANDS = [
    'add task', 'list tasks', 'complete task', 'delete task', 'update task',
    'add habit', 'list habits', 'mark habit',
    'start focus', 'show summary', 'help', 'exit', 'quit'
]

console = Console()
session = PromptSession()
completer = WordCompleter(COMMANDS, ignore_case=True)

def print_help():
    console.print("""
[bold underline]Personal Productivity Assistant CLI Commands[/bold underline]
- add task "Task Title" --priority [low|medium|high] --due YYYY-MM-DD
- list tasks [--all]
- complete task TASK_ID
- delete task TASK_ID
- update task TASK_ID [--title "New Title"] [--priority ...] [--due ...]
- add habit "Habit Name"
- list habits
- mark habit HABIT_ID
- start focus [--minutes N] [--break N] [--cycles N]
- show summary
- help
- exit / quit
""")

def main():
    init_db()
    task_manager = TaskManager()
    habit_tracker = HabitTracker()
    focus_timer = FocusTimer()
    summary = Summary()
    print_help()
    while True:
        try:
            user_input = session.prompt('> ', completer=completer).strip()
        except (EOFError, KeyboardInterrupt):
            console.print("\n[bold]Goodbye![/bold]")
            break
        if not user_input:
            continue
        cmd = user_input.lower()
        if cmd in ('exit', 'quit'):
            console.print("[bold]Goodbye![/bold]")
            break
        elif cmd.startswith('add task'):
            import shlex
            args = shlex.split(user_input)
            title = args[2] if len(args) > 2 else ''
            priority = 'medium'
            due = None
            for i, arg in enumerate(args):
                if arg == '--priority' and i+1 < len(args):
                    priority = args[i+1]
                if arg == '--due' and i+1 < len(args):
                    due = args[i+1]
            if not title:
                console.print("[red]Task title required.[/red]")
                continue
            try:
                if due:
                    parse_date(due)
                task_id = task_manager.add_task(title, priority, due)
                console.print(f"[green]Task added (ID: {task_id})[/green]")
            except Exception as e:
                console.print(f"[red]Error: {e}[/red]")
        elif cmd.startswith('list tasks'):
            show_all = '--all' in user_input
            tasks = task_manager.list_tasks(show_all)
            if not tasks:
                console.print("[yellow]No tasks found.[/yellow]")
            for t in tasks:
                status = '[x]' if t['completed'] else '[ ]'
                due = t['due_date'] or '-'
                console.print(f"{status} {t['id']}: {t['title']} (Priority: {t['priority']}, Due: {due})")
        elif cmd.startswith('complete task'):
            try:
                task_id = int(user_input.split()[-1])
                if task_manager.complete_task(task_id):
                    console.print(f"[green]Task {task_id} marked complete.[/green]")
                else:
                    console.print(f"[red]Task {task_id} not found.[/red]")
            except Exception:
                console.print("[red]Usage: complete task TASK_ID[/red]")
        elif cmd.startswith('delete task'):
            try:
                task_id = int(user_input.split()[-1])
                if task_manager.delete_task(task_id):
                    console.print(f"[green]Task {task_id} deleted.[/green]")
                else:
                    console.print(f"[red]Task {task_id} not found.[/red]")
            except Exception:
                console.print("[red]Usage: delete task TASK_ID[/red]")
        elif cmd.startswith('update task'):
            import shlex
            args = shlex.split(user_input)
            if len(args) < 3:
                console.print("[red]Usage: update task TASK_ID [--title ...] [--priority ...] [--due ...][/red]")
                continue
            try:
                task_id = int(args[2])
            except Exception:
                console.print("[red]Invalid TASK_ID.[/red]")
                continue
            title = None
            priority = None
            due = None
            for i, arg in enumerate(args):
                if arg == '--title' and i+1 < len(args):
                    title = args[i+1]
                if arg == '--priority' and i+1 < len(args):
                    priority = args[i+1]
                if arg == '--due' and i+1 < len(args):
                    due = args[i+1]
            if due:
                try:
                    parse_date(due)
                except Exception:
                    console.print("[red]Invalid due date format.[/red]")
                    continue
            if task_manager.update_task(task_id, title, priority, due):
                console.print(f"[green]Task {task_id} updated.[/green]")
            else:
                console.print(f"[red]Task {task_id} not found or update failed.[/red]")
        elif cmd.startswith('add habit'):
            import shlex
            args = shlex.split(user_input)
            if len(args) < 3:
                console.print("[red]Usage: add habit \"Habit Name\"[/red]")
                continue
            name = args[2]
            habit_id = habit_tracker.add_habit(name)
            console.print(f"[green]Habit added (ID: {habit_id})[/green]")
        elif cmd.startswith('list habits'):
            habits = habit_tracker.list_habits()
            if not habits:
                console.print("[yellow]No habits found.[/yellow]")
            for h in habits:
                streak = h['streak']
                done = '[x]' if h['last_completed'] == str(__import__('datetime').date.today()) else '[ ]'
                console.print(f"{done} {h['id']}: {h['name']} (Streak: {streak})")
        elif cmd.startswith('mark habit'):
            try:
                habit_id = int(user_input.split()[-1])
                if habit_tracker.mark_habit(habit_id):
                    console.print(f"[green]Habit {habit_id} marked for today.[/green]")
                else:
                    console.print(f"[red]Habit {habit_id} not found or already marked today.[/red]")
            except Exception:
                console.print("[red]Usage: mark habit HABIT_ID[/red]")
        elif cmd.startswith('start focus'):
            import shlex
            args = shlex.split(user_input)
            minutes = 25
            break_minutes = 5
            cycles = 1
            for i, arg in enumerate(args):
                if arg == '--minutes' and i+1 < len(args):
                    minutes = int(args[i+1])
                if arg == '--break' and i+1 < len(args):
                    break_minutes = int(args[i+1])
                if arg == '--cycles' and i+1 < len(args):
                    cycles = int(args[i+1])
            focus_timer.start_focus(minutes, break_minutes, cycles)
        elif cmd.startswith('show summary'):
            console.print(summary.daily_summary())
        elif cmd == 'help':
            print_help()
        else:
            console.print("[red]Unknown command. Type 'help' for available commands.[/red]")

if __name__ == '__main__':
    main()
