from datetime import date

from . import index, storage
from .models import Article


class NotFoundError(Exception):
    pass


def get_article(articles_dir, article_id: str) -> Article:
    path = storage.article_path(articles_dir, article_id)
    if not path.exists():
        raise NotFoundError(article_id)
    return storage.read_article(path)


def add_article(
    articles_dir,
    conn,
    *,
    title: str,
    media_type: str,
    summary: str = "",
    tags: list[str] | None = None,
    references: list[str] | None = None,
    images: list[str] | None = None,
    published_date: str | None = None,
    body: str = "",
) -> Article:
    article = Article(
        id=storage.generate_id(),
        title=title,
        media_type=media_type,
        summary=summary,
        tags=tags or [],
        references=references or [],
        images=images or [],
        published_date=published_date or date.today().isoformat(),
        created_at=date.today().isoformat(),
        body=body,
    )
    storage.write_article(articles_dir, article)
    index.upsert_article(conn, article)
    return article


def edit_article(
    articles_dir,
    conn,
    article_id: str,
    *,
    title: str | None = None,
    media_type: str | None = None,
    summary: str | None = None,
    tags: list[str] | None = None,
    references: list[str] | None = None,
    images: list[str] | None = None,
    published_date: str | None = None,
    body: str | None = None,
) -> Article:
    article = get_article(articles_dir, article_id)

    if title is not None:
        article.title = title
    if media_type is not None:
        article.media_type = media_type
    if summary is not None:
        article.summary = summary
    if tags is not None:
        article.tags = tags
    if references is not None:
        article.references = references
    if images is not None:
        article.images = images
    if published_date is not None:
        article.published_date = published_date
    if body is not None:
        article.body = body

    storage.write_article(articles_dir, article)
    index.upsert_article(conn, article)
    return article


def delete_article(articles_dir, conn, article_id: str) -> None:
    path = storage.article_path(articles_dir, article_id)
    if not path.exists():
        raise NotFoundError(article_id)
    storage.delete_article_file(articles_dir, article_id)
    index.delete_article(conn, article_id)


def list_articles(conn):
    return index.list_all(conn)


def search_articles(conn, tag: str | None = None, title: str | None = None):
    return index.search(conn, tag=tag, title=title)


def reindex(conn, articles_dir) -> int:
    return index.rebuild_index(conn, articles_dir)
