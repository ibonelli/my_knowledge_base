import pytest

from article_catalog import core, index, storage


def _connect(tmp_path):
    return index.connect(str(tmp_path / "catalog.db"))


def test_add_list_search_edit_delete_reindex(tmp_path):
    conn = _connect(tmp_path)
    articles_dir = tmp_path / "articles"

    article = core.add_article(
        articles_dir,
        conn,
        title="My Article",
        media_type="written",
        tags=["ai", "AI"],
    )
    assert [row[0] for row in core.list_articles(conn)] == [article.id]
    assert [row[0] for row in core.search_articles(conn, tag="ai")] == [article.id]
    assert core.search_articles(conn, title="nonexistent") == []

    updated = core.edit_article(articles_dir, conn, article.id, title="My Article (Updated)")
    assert updated.title == "My Article (Updated)"
    assert [row[1] for row in core.list_articles(conn)] == ["My Article (Updated)"]

    count = core.reindex(conn, articles_dir)
    assert count == 1

    core.delete_article(articles_dir, conn, article.id)
    assert core.list_articles(conn) == []


def test_add_article_rejects_invalid_media_type(tmp_path):
    conn = _connect(tmp_path)
    with pytest.raises(storage.ValidationError):
        core.add_article(tmp_path / "articles", conn, title="x", media_type="podcast")


def test_edit_nonexistent_article_raises_not_found(tmp_path):
    conn = _connect(tmp_path)
    with pytest.raises(core.NotFoundError):
        core.edit_article(tmp_path / "articles", conn, "doesnotexist", title="x")


def test_delete_nonexistent_article_raises_not_found(tmp_path):
    conn = _connect(tmp_path)
    with pytest.raises(core.NotFoundError):
        core.delete_article(tmp_path / "articles", conn, "doesnotexist")


def test_backfill_with_historical_published_date(tmp_path):
    conn = _connect(tmp_path)
    article = core.add_article(
        tmp_path / "articles",
        conn,
        title="Old Piece",
        media_type="graphic",
        published_date="2015-06-01",
    )
    assert article.published_date == "2015-06-01"
    rows = core.list_articles(conn)
    assert rows[0][3] == "2015-06-01"
