import sqlite3
import os
from datetime import datetime
from models.task import Task

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "tasks.db")

def init_db():
    if not os.path.exists(os.path.dirname(DB_PATH)):
        os.makedirs(os.path.dirname(DB_PATH))
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                due_date TEXT,
                priority TEXT,
                labels TEXT,
                completed INTEGER DEFAULT 0,
                created_at TEXT
            )
        ''')
        conn.commit()

def add_task(task: Task) -> int:
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        created_at = datetime.now().isoformat()
        cursor.execute('''
            INSERT INTO tasks (title, description, due_date, priority, labels, completed, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (task.title, task.description, task.due_date, task.priority, task.labels, int(task.completed), created_at))
        conn.commit()
        return cursor.lastrowid

def update_task(task: Task):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE tasks
            SET title = ?, description = ?, due_date = ?, priority = ?, labels = ?, completed = ?
            WHERE id = ?
        ''', (task.title, task.description, task.due_date, task.priority, task.labels, int(task.completed), task.id))
        conn.commit()

def delete_task(task_id: int):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        conn.commit()

def toggle_complete(task_id: int, completed: bool):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE tasks SET completed = ? WHERE id = ?', (int(completed), task_id))
        conn.commit()

def get_tasks(filter_type: str = "All", search_query: str = "") -> list[Task]:
    query = "SELECT id, title, description, due_date, priority, labels, completed, created_at FROM tasks WHERE 1=1"
    params = []

    if filter_type == "Completed":
        query += " AND completed = 1"
    elif filter_type == "All":
        pass
    elif filter_type == "Today":
        today = datetime.now().strftime("%Y-%m-%d")
        query += " AND due_date = ?"
        params.append(today)
    elif filter_type == "Upcoming":
        today = datetime.now().strftime("%Y-%m-%d")
        query += " AND due_date > ? AND completed = 0"
        params.append(today)
    elif filter_type in ["High", "Medium", "Low"]:
        query += " AND priority = ?"
        params.append(filter_type)

    if search_query:
        query += " AND (title LIKE ? OR description LIKE ? OR labels LIKE ?)"
        params.extend([f"%{search_query}%", f"%{search_query}%", f"%{search_query}%"])

    query += " ORDER BY completed ASC, due_date ASC, created_at DESC"

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()

    tasks = []
    for row in rows:
        tasks.append(Task(
            id=row[0],
            title=row[1],
            description=row[2],
            due_date=row[3],
            priority=row[4],
            labels=row[5],
            completed=bool(row[6]),
            created_at=row[7]
        ))
    return tasks
