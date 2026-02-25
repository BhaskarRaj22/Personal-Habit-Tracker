# Personal Productivity Assistant

An advanced CLI-based productivity assistant to help you manage tasks, goals, habits, focus sessions, and daily summaries.

## Features
- **Task Manager**: Add, update, delete, complete tasks with priority and due dates
- **Habit Tracker**: Track habits, view streaks, and mark daily completions
- **Focus Timer**: Pomodoro-style focus sessions with break reminders
- **Daily Summary**: Get a summary of your productivity, completed tasks, and habit streaks
- **Persistent Storage**: All data is stored locally using SQLite for reliability and speed
- **Command-based CLI**: Intuitive commands for all features

## CLI Command Examples
- `add task "Finish report" --priority high --due 2026-02-10`
- `list tasks --all`
- `complete task 3`
- `add habit "Read 20 pages"`
- `mark habit 2`
- `show habits`
- `start focus --minutes 25`
- `show summary`

## Installation
1. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```

## How to Run
```sh
python main.py
```

## Data Storage
- All data (tasks, habits, focus sessions) is stored in a local SQLite database (`assistant.db`).
- No data leaves your machine. Safe, private, and persistent.

## How to Fork and Customize
- Fork this repository on GitHub
- Modify or extend any module (e.g., add new commands, change storage backend)

