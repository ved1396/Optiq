import logging
import sqlite3
from pathlib import Path
from typing import Iterable

import pandas as pd

from config import settings

logger = logging.getLogger(__name__)


def get_db_path() -> str:
    database_url = settings.database_url
    if database_url.startswith("sqlite:///"):
        return database_url.removeprefix("sqlite:///")
    if database_url.startswith("sqlite://"):
        return database_url.removeprefix("sqlite://")
    return database_url


DB_PATH = Path(get_db_path())


def get_db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def _existing_columns(cursor: sqlite3.Cursor, table_name: str) -> set[str]:
    cursor.execute(f"PRAGMA table_info({table_name})")
    return {row[1] for row in cursor.fetchall()}


def _add_missing_columns(cursor: sqlite3.Cursor, table_name: str, statements: Iterable[str]) -> None:
    existing = _existing_columns(cursor, table_name)
    for statement in statements:
        column_name = statement.split()[0]
        if column_name not in existing:
            cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {statement}")


def init_db() -> None:
    """Initialize database tables and backfill missing columns for local upgrades."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS queries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query TEXT NOT NULL,
                route TEXT NOT NULL,
                response TEXT,
                latency_ms REAL NOT NULL,
                estimated_cost REAL NOT NULL,
                estimated_energy REAL NOT NULL,
                confidence_score REAL DEFAULT 0,
                classifier_label TEXT,
                heuristic_route TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        _add_missing_columns(
            cursor,
            "queries",
            [
                "response TEXT",
                "confidence_score REAL DEFAULT 0",
                "classifier_label TEXT",
                "heuristic_route TEXT",
                "created_at DATETIME DEFAULT CURRENT_TIMESTAMP",
            ],
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS analytics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query_id INTEGER NOT NULL,
                query TEXT NOT NULL,
                route TEXT NOT NULL,
                latency_ms REAL NOT NULL,
                estimated_cost REAL NOT NULL,
                estimated_energy REAL NOT NULL,
                confidence_score REAL DEFAULT 0,
                feedback_rating INTEGER,
                feedback_comments TEXT,
                correct_route TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(query_id) REFERENCES queries(id)
            )
            """
        )
        _add_missing_columns(
            cursor,
            "analytics",
            [
                "confidence_score REAL DEFAULT 0",
                "feedback_rating INTEGER",
                "feedback_comments TEXT",
                "correct_route TEXT",
                "timestamp DATETIME DEFAULT CURRENT_TIMESTAMP",
            ],
        )

        cursor.execute("CREATE INDEX IF NOT EXISTS idx_queries_created_at ON queries(created_at)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_queries_route ON queries(route)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_analytics_timestamp ON analytics(timestamp)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_analytics_query_id ON analytics(query_id)")
        conn.commit()
    logger.info("SQLite database ready at %s", DB_PATH)


def read_dataframe(sql: str, params: tuple | None = None) -> pd.DataFrame:
    with get_db_connection() as conn:
        return pd.read_sql_query(sql, conn, params=params or ())
