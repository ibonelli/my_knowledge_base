from pathlib import Path

import pytest

from article_fetcher import cli
from article_fetcher.frontmatter import parse_markdown


def test_cli_end_to_end_saves_article(local_server, tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("EDITOR", "true")  # POSIX no-op: exits 0 without touching the file

    output_dir = tmp_path / "imported"
    cli.main(
        [
            f"{local_server}/good_article.html",
            "--output-dir",
            str(output_dir),
            "--tag",
            "test",
            "--yes",
        ]
    )

    saved = list(output_dir.glob("*.md"))
    assert len(saved) == 1

    meta, body = parse_markdown(saved[0].read_text(encoding="utf-8"))
    assert meta["media_type"] == "written"
    assert meta["tags"] == ["test"]
    assert meta["references"] == [f"{local_server}/good_article.html"]
    assert meta["summary"] == ""
    assert "local-first" in body.lower()

    out = capsys.readouterr().out
    assert "saved" in out


def test_cli_aborts_without_yes_when_not_confirmed(local_server, tmp_path, monkeypatch):
    monkeypatch.setenv("EDITOR", "true")
    monkeypatch.setattr("builtins.input", lambda _prompt: "n")

    output_dir = tmp_path / "imported"
    cli.main([f"{local_server}/good_article.html", "--output-dir", str(output_dir)])

    assert list(output_dir.glob("*.md")) == []


def test_cli_fetch_error_exits_before_editor(tmp_path, monkeypatch):
    def _boom(*args, **kwargs):
        raise AssertionError("editor should not be invoked when the fetch fails")

    monkeypatch.setattr("article_fetcher.editor.edit_in_editor", _boom)

    with pytest.raises(SystemExit) as exc_info:
        cli.main(["not-a-valid-url", "--output-dir", str(tmp_path / "imported")])

    assert exc_info.value.code == 1
