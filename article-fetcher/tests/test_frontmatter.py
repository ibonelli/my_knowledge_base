import pytest

from article_fetcher import frontmatter


def test_generate_id_shape():
    article_id = frontmatter.generate_id()
    assert len(article_id) == 8
    int(article_id, 16)  # hex


def test_render_and_parse_round_trip():
    meta = frontmatter.build_front_matter(
        article_id="abc123",
        title="Test Article",
        summary="",
        media_type="written",
        tags=["ai"],
        references=["https://example.com"],
        images=[],
        published_date="2024-01-01",
        created_at="2024-01-02",
    )
    text = frontmatter.render_markdown(meta, "Hello world")

    parsed_meta, body = frontmatter.parse_markdown(text)
    assert parsed_meta["title"] == "Test Article"
    assert parsed_meta["references"] == ["https://example.com"]
    assert "Hello world" in body


def test_parse_markdown_requires_front_matter():
    with pytest.raises(ValueError):
        frontmatter.parse_markdown("no front matter here")


def test_validate_front_matter_requires_title():
    with pytest.raises(ValueError):
        frontmatter.validate_front_matter({"title": "", "media_type": "written"})


def test_validate_front_matter_requires_known_media_type():
    with pytest.raises(ValueError):
        frontmatter.validate_front_matter({"title": "x", "media_type": "podcast"})


def test_validate_front_matter_accepts_valid_input():
    frontmatter.validate_front_matter({"title": "x", "media_type": "graphic"})
