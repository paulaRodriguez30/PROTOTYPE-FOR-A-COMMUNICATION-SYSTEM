import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from .core.config import BASE_DIR

DB_PATH = (BASE_DIR / "runs.sqlite3").resolve()

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    cur = conn.cursor()
    
    # Crear tabla si no existe
    cur.execute("""
    CREATE TABLE IF NOT EXISTS runs (
        id TEXT PRIMARY KEY,
        mode TEXT DEFAULT 'image',
        user_role TEXT DEFAULT 'doctor',
        filename TEXT,
        stored_path TEXT,
        text_content TEXT,
        status TEXT NOT NULL,
        created_at TEXT NOT NULL,
        finished_at TEXT,
        log_path TEXT
    )
    """)
    
    # Migración: añadir columnas si no existen
    columns_to_add = [
        ('mode', 'TEXT DEFAULT "image"'),
        ('user_role', 'TEXT DEFAULT "doctor"'),
        ('text_content', 'TEXT')
    ]
    
    for column_name, column_type in columns_to_add:
        try:
            cur.execute(f"ALTER TABLE runs ADD COLUMN {column_name} {column_type}")
            print(f"✓ Columna '{column_name}' añadida")
        except sqlite3.OperationalError:
            pass  # La columna ya existe
    
    conn.commit()
    conn.close()
    print("✓ Base de datos inicializada")

def now_utc():
    return datetime.now(timezone.utc).isoformat()

def create_run(
    run_id: str,
    filename: str,
    stored_path: str,
    status: str,
    log_path: str,
    mode: str = "image",
    user_role: str = "doctor",
    text_content: Optional[str] = None
):
    conn = get_conn()
    cur = conn.cursor()
    
    cur.execute(
        """INSERT INTO runs 
           (id, mode, user_role, filename, stored_path, text_content, status, created_at, log_path) 
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (run_id, mode, user_role, filename, stored_path, text_content, status, now_utc(), log_path),
    )
    conn.commit()
    conn.close()

def update_status(run_id: str, status: str, finished: bool = False):
    conn = get_conn()
    cur = conn.cursor()
    if finished:
        cur.execute(
            "UPDATE runs SET status = ?, finished_at = ? WHERE id = ?",
            (status, now_utc(), run_id),
        )
    else:
        cur.execute(
            "UPDATE runs SET status = ? WHERE id = ?",
            (status, run_id),
        )
    conn.commit()
    conn.close()

def get_run(run_id: str):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM runs WHERE id = ?", (run_id,))
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None