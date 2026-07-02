import sqlite3

from .models import Article
from .storage import iter_article_files, read_article

SCHEMA = """
CREATE TABLE IF NOT EXISTS articles (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    summary TEXT,
    media_type TEXT NOT NULL,
    file_path TEXT NOT NULL,
    published_date TEXT,
    created_at TEXT
);
CREATE TABLE IF NOT EXISTS tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);
CREATE TABLE IF NOT EXISTS article_tags (
    article_id TEXT NOT NULL REFERENCES articles(id) ON DELETE CASCADE,
    tag_id INTEGER NOT NULL REFERENCES tags(id) ON DELETE CASCADE,
    PRIMARY KEY (article_id, tag_id)
);
"""


def connect(db_path) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript(SCHEMA)
    return conn


def _get_or_create_tag(conn: sqlite3.Connection, name: str) -> int:
    row = conn.execute("SELECT id FROM tags WHERE name = ?", (name,)).fetchone()
    if row:
        return row[0]
    cursor = conn.execute("INSERT INTO tags(name) VALUES (?)", (name,))
    return cursor.lastrowid


def upsert_article(conn: sqlite3.Connection, article: Article) -> None:
    conn.execute(
        """
        INSERT INTO articles (id, title, summary, media_type, file_path, published_date, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            title = excluded.title,
            summary = excluded.summary,
            media_type = excluded.media_type,
            file_path = excluded.file_path,
            published_date = excluded.published_date,
            created_at = excluded.created_at
        """,
        (
            article.id,
            article.title,
            article.summary,
            article.media_type,
            article.file_path,
            article.published_date,
            article.created_at,
        ),
    )
    conn.execute("DELETE FROM article_tags WHERE article_id = ?", (article.id,))
    for tag_name in article.tags:
        tag_id = _get_or_create_tag(conn, tag_name)
        conn.execute(
            "INSERT OR IGNORE INTO article_tags (article_id, tag_id) VALUES (?, ?)",
            (article.id, tag_id),
        )
    conn.commit()


def delete_article(conn: sqlite3.Connection, article_id: str) -> None:
    conn.execute("DELETE FROM articles WHERE id = ?", (article_id,))
    conn.commit()


def rebuild_index(conn: sqlite3.Connection, articles_dir) -> int:
    conn.execute("DELETE FROM article_tags")
    conn.execute("DELETE FROM tags")
    conn.execute("DELETE FROM articles")
    conn.commit()

    count = 0
    for path in iter_article_files(articles_dir):
        article = read_article(path)
        upsert_article(conn, article)
        count += 1
    return count


def list_all(conn: sqlite3.Connection):
    return conn.execute(
        "SELECT id, title, media_type, published_date, file_path "
        "FROM articles ORDER BY published_date, created_at"
    ).fetchall()


def search(conn: sqlite3.Connection, tag: str | None = None, title: str | None = None):
    query = "SELECT DISTINCT a.id, a.title, a.media_type, a.published_date, a.file_path FROM articles a"
    conditions = []
    params: list[str] = []

    if tag:
        query += " JOIN article_tags at ON at.article_id = a.id JOIN tags t ON t.id = at.tag_id"
        conditions.append("t.name = ?")
        params.append(tag.strip().lower())

    if title:
        conditions.append("a.title LIKE ?")
        params.append(f"%{title}%")

    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    query += " ORDER BY a.published_date, a.created_at"

    return conn.execute(query, params).fetchall()
