import pytest

from article_catalog import storage
from article_catalog.models import Article


def test_write_and_read_article_round_trip(tmp_path):
    article = Article(
        id="abc123",
        title="Test Article",
        media_type="written",
        tags=["AI", "ai", " Tools "],
        references=["https://example.com"],
        body="Hello world",
    )
    storage.write_article(tmp_path, article)

    path = storage.article_path(tmp_path, "abc123")
    assert path.exists()

    loaded = storage.read_article(path)
    assert loaded.title == "Test Article"
    assert loaded.tags == ["ai", "tools"]
    assert loaded.references == ["https://example.com"]
    assert "Hello world" in loaded.body


def test_write_article_requires_title(tmp_path):
    article = Article(id="x", title="", media_type="written")
    with pytest.raises(storage.ValidationError):
        storage.write_article(tmp_path, article)


def test_write_article_requires_valid_media_type(tmp_path):
    article = Article(id="x", title="Test", media_type="podcast")
    with pytest.raises(storage.ValidationError):
        storage.write_article(tmp_path, article)


def test_delete_article_file(tmp_path):
    article = Article(id="x", title="Test", media_type="graphic")
    storage.write_article(tmp_path, article)
    assert storage.article_path(tmp_path, "x").exists()

    storage.delete_article_file(tmp_path, "x")
    assert not storage.article_path(tmp_path, "x").exists()


def test_iter_article_files_on_missing_dir(tmp_path):
    missing = tmp_path / "does-not-exist"
    assert storage.iter_article_files(missing) == []
