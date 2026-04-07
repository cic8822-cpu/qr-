import sqlite3
from datetime import datetime
from pathlib import Path
import os

# 사용자 홈 디렉토리에 표준화된 경로로 저장
DB_PATH = Path(os.path.expanduser("~")) / ".qr_generator" / "urls.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)


def get_db():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_url TEXT NOT NULL,
            short_code TEXT UNIQUE NOT NULL,
            custom_alias TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            expires_at DATETIME,
            click_count INTEGER DEFAULT 0
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analytics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url_id INTEGER NOT NULL,
            ip_address TEXT,
            user_agent TEXT,
            clicked_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (url_id) REFERENCES urls (id)
        )
    """)

    conn.commit()
    conn.close()


def create_url(
    original_url: str, short_code: str, custom_alias: str = None, expires_at: str = None
):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO urls (original_url, short_code, custom_alias, expires_at) VALUES (?, ?, ?, ?)",
        (original_url, short_code, custom_alias, expires_at),
    )
    conn.commit()
    conn.close()


def get_url_by_code(short_code: str):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM urls WHERE short_code = ?", (short_code,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def get_url_by_alias(alias: str):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM urls WHERE custom_alias = ?", (alias,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def increment_click(short_code: str):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE urls SET click_count = click_count + 1 WHERE short_code = ?",
        (short_code,),
    )
    conn.commit()
    conn.close()


def record_analytics(url_id: int, ip_address: str, user_agent: str):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO analytics (url_id, ip_address, user_agent) VALUES (?, ?, ?)",
        (url_id, ip_address, user_agent),
    )
    conn.commit()
    conn.close()


def get_stats(short_code: str):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM urls WHERE short_code = ?", (short_code,))
    url = cursor.fetchone()

    if not url:
        conn.close()
        return None

    cursor.execute(
        "SELECT ip_address, user_agent, clicked_at FROM analytics WHERE url_id = ? ORDER BY clicked_at DESC",
        (url["id"],),
    )
    clicks = cursor.fetchall()

    conn.close()

    return {
        "original_url": url["original_url"],
        "short_code": url["short_code"],
        "custom_alias": url["custom_alias"],
        "created_at": url["created_at"],
        "expires_at": url["expires_at"],
        "click_count": url["click_count"],
        "clicks": [dict(c) for c in clicks],
    }
