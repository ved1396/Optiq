import sqlite3
import logging
from config import settings

logger = logging.getLogger(__name__)


def get_db_path() -> str:
    database_url = getattr(settings, "database_url", "sqlite:///./optiq.db")
    if database_url.startswith("sqlite:///"):
        return database_url[len("sqlite:///"):]
    if database_url.startswith("sqlite://"):
        return database_url[len("sqlite://"):]
    return database_url

DB_PATH = get_db_path()

def init_db():
    """Initializes the SQLite database and creates necessary tables."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create queries table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS queries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        query TEXT NOT NULL,
        route TEXT NOT NULL,
        response TEXT,
        latency_ms REAL,
        estimated_cost REAL,
        estimated_energy REAL,
        confidence_score REAL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Create feedback table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        query_id INTEGER,
        rating INTEGER,
        comments TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(query_id) REFERENCES queries(id)
    )
    ''')
    
    conn.commit()
    conn.close()
    logger.info("Database initialized successfully.")

def get_db_connection():
    """Returns a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn
