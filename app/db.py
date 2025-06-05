import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
from app.config import settings

@contextmanager
def get_db_connection():
    conn = psycopg2.connect(settings.DATABASE_URL, cursor_factory=RealDictCursor)
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS calls (
                    id SERIAL PRIMARY KEY,
                    caller_number VARCHAR(20),
                    call_type VARCHAR(10),
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    intent VARCHAR(50),
                    ticket_id VARCHAR(50)
                );
            """)
            conn.commit()

def save_call_metadata(caller_number: str, call_type: str, intent: str, ticket_id: str = None):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO calls (caller_number, call_type, intent, ticket_id)
                VALUES (%s, %s, %s, %s) RETURNING id;
                """,
                (caller_number, call_type, intent, ticket_id)
            )
            conn.commit()
            return cur.fetchone()['id']
