from article_catalog import index, storage
from article_catalog.models import Article


def test_upsert_and_search_by_tag_and_title(tmp_path):
    conn = index.connect(str(tmp_path / "catalog.db"))
    article = Article(
        id="a1",
        title="Learning Python",
        media_type="written",
        tags=["python", "learning"],
        published_date="2024-01-01",
        created_at="2024-01-01",
        file_path=str(tmp_path / "a1.md"),
    )
    index.upsert_article(conn, article)

    rows = index.search(conn, tag="python")
    assert [row[0] for row in rows] == ["a1"]

    rows = index.search(conn, title="learning")
    assert [row[0] for row in rows] == ["a1"]

    assert index.search(conn, tag="nonexistent") == []


def test_rebuild_index_scans_markdown_files(tmp_path):
    articles_dir = tmp_path / "articles"
    article = Article(
        id="a1",
        title="Video Piece",
        media_type="video",
        tags=["clips"],
        published_date="2023-05-01",
        created_at="2023-05-01",
    )
    storage.write_article(articles_dir, article)

    conn = index.connect(str(tmp_path / "catalog.db"))
    count = index.rebuild_index(conn, articles_dir)

    assert count == 1
    rows = index.list_all(conn)
    assert rows[0][0] == "a1"


def test_delete_removes_from_index(tmp_path):
    conn = index.connect(str(tmp_path / "catalog.db"))
    article = Article(id="a1", title="To Delete", media_type="graphic", file_path="a1.md")
    index.upsert_article(conn, article)

    index.delete_article(conn, "a1")

    assert index.list_all(conn) == []


def test_upsert_replaces_tags_on_update(tmp_path):
    conn = index.connect(str(tmp_path / "catalog.db"))
    article = Article(id="a1", title="Piece", media_type="written", tags=["old"], file_path="a1.md")
    index.upsert_article(conn, article)

    article.tags = ["new"]
    index.upsert_article(conn, article)

    assert index.search(conn, tag="old") == []
    assert [row[0] for row in index.search(conn, tag="new")] == ["a1"]
