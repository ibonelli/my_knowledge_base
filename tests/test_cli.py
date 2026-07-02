from article_catalog.cli import main


def _run(common, *args):
    main(common + list(args))


def test_add_list_search_edit_delete_reindex(tmp_path, capsys):
    articles_dir = tmp_path / "articles"
    db_path = tmp_path / "catalog.db"
    common = ["--articles-dir", str(articles_dir), "--db", str(db_path)]

    _run(common, "add", "--title", "My Article", "--media-type", "written", "--tag", "ai", "--tag", "AI")
    out = capsys.readouterr().out
    assert "added" in out
    article_id = out.split()[1].rstrip(":")

    _run(common, "list")
    assert "My Article" in capsys.readouterr().out

    _run(common, "search", "--tag", "ai")
    assert "My Article" in capsys.readouterr().out

    _run(common, "search", "--title", "nonexistent")
    assert "no articles found" in capsys.readouterr().out

    _run(common, "edit", article_id, "--title", "My Article (Updated)")
    assert "updated" in capsys.readouterr().out

    _run(common, "list")
    assert "My Article (Updated)" in capsys.readouterr().out

    _run(common, "reindex")
    assert "reindexed 1 article" in capsys.readouterr().out

    _run(common, "delete", article_id)
    assert "deleted" in capsys.readouterr().out

    _run(common, "list")
    assert "no articles found" in capsys.readouterr().out


def test_backfill_with_historical_published_date(tmp_path, capsys):
    articles_dir = tmp_path / "articles"
    db_path = tmp_path / "catalog.db"
    common = ["--articles-dir", str(articles_dir), "--db", str(db_path)]

    _run(
        common,
        "add",
        "--title",
        "Old Piece",
        "--media-type",
        "graphic",
        "--published-date",
        "2015-06-01",
    )
    capsys.readouterr()

    _run(common, "list")
    out = capsys.readouterr().out
    assert "2015-06-01" in out


def test_edit_nonexistent_article_errors(tmp_path, capsys):
    articles_dir = tmp_path / "articles"
    db_path = tmp_path / "catalog.db"
    common = ["--articles-dir", str(articles_dir), "--db", str(db_path)]

    try:
        _run(common, "edit", "doesnotexist", "--title", "x")
        assert False, "expected SystemExit"
    except SystemExit as exc:
        assert exc.code == 1
    assert "not found" in capsys.readouterr().err
