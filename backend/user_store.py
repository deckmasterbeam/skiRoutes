import importlib
import os
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = Path('/tmp/users.db') if os.getenv('VERCEL') else BASE_DIR / 'users.db'
POSTGRES_URL = (
    os.getenv('DATABASE_URL')
    or os.getenv('POSTGRES_URL_NON_POOLING')
    or os.getenv('POSTGRES_URL')
)
USE_POSTGRES = bool(POSTGRES_URL)


def _create_login_events_table_postgres(cur) -> None:
    cur.execute('''CREATE TABLE IF NOT EXISTS userLogins (
        id BIGSERIAL PRIMARY KEY,
        sub TEXT NOT NULL,
        email TEXT,
        name TEXT,
        raw_json TEXT,
        logged_in_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    )''')


def _create_login_events_table_sqlite(cur) -> None:
    cur.execute('''CREATE TABLE IF NOT EXISTS userLogins (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sub TEXT NOT NULL,
        email TEXT,
        name TEXT,
        raw_json TEXT,
        logged_in_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
    )''')


def init_db_postgres() -> None:
    psycopg = importlib.import_module('psycopg')
    with psycopg.connect(POSTGRES_URL) as conn:
        with conn.cursor() as cur:
            _create_login_events_table_postgres(cur)

            # Legacy table schema used `sub` as the primary key.
            cur.execute('''
                SELECT 1
                FROM information_schema.columns
                WHERE table_schema = 'public'
                  AND table_name = 'userlogins'
                  AND column_name = 'id'
            ''')
            has_id_column = cur.fetchone() is not None

            if not has_id_column:
                cur.execute('ALTER TABLE userLogins RENAME TO userLogins_legacy')
                _create_login_events_table_postgres(cur)
                cur.execute('''
                    INSERT INTO userLogins (sub, email, name, raw_json)
                    SELECT sub, email, name, raw_json
                    FROM userLogins_legacy
                ''')
                cur.execute('DROP TABLE userLogins_legacy')
        conn.commit()


def init_db_sqlite() -> None:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    _create_login_events_table_sqlite(c)

    # Legacy table schema used `sub` as the primary key.
    c.execute('PRAGMA table_info(userLogins)')
    columns = c.fetchall()
    has_id_column = any(column[1] == 'id' for column in columns)

    if not has_id_column and columns:
        c.execute('ALTER TABLE userLogins RENAME TO userLogins_legacy')
        _create_login_events_table_sqlite(c)
        c.execute('''
            INSERT INTO userLogins (sub, email, name, raw_json)
            SELECT sub, email, name, raw_json
            FROM userLogins_legacy
        ''')
        c.execute('DROP TABLE userLogins_legacy')

    conn.commit()
    conn.close()


def init_db() -> None:
    if USE_POSTGRES:
        init_db_postgres()
        return

    init_db_sqlite()


def insert_login_postgres(sub: str, email: str | None, name: str | None, raw_json: str) -> None:
    psycopg = importlib.import_module('psycopg')
    with psycopg.connect(POSTGRES_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(
                '''INSERT INTO userLogins (sub, email, name, raw_json)
                   VALUES (%s, %s, %s, %s)''',
                (sub, email, name, raw_json),
            )
        conn.commit()


def insert_login_sqlite(sub: str, email: str | None, name: str | None, raw_json: str) -> None:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        '''INSERT INTO userLogins (sub, email, name, raw_json)
           VALUES (?, ?, ?, ?)''',
        (sub, email, name, raw_json),
    )
    conn.commit()
    conn.close()


def insert_login(sub: str, email: str | None, name: str | None, raw_json: str) -> None:
    if USE_POSTGRES:
        insert_login_postgres(sub, email, name, raw_json)
        return

    insert_login_sqlite(sub, email, name, raw_json)
