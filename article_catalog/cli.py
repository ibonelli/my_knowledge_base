import argparse
import sys
from datetime import date
from pathlib import Path

from . import index, storage
from .models import MEDIA_TYPES, Article

DEFAULT_ARTICLES_DIR = "articles"
DEFAULT_DB_PATH = "catalog.db"


def _read_body(body_file: str | None) -> str:
    if body_file is None:
        return ""
    if body_file == "-":
        return sys.stdin.read()
    return Path(body_file).read_text(encoding="utf-8")


def _print_rows(rows) -> None:
    if not rows:
        print("no articles found")
        return
    for article_id, title, media_type, published_date, file_path in rows:
        print(f"{article_id}  [{media_type}]  {published_date or '-'}  {title}  ({file_path})")


def cmd_add(args: argparse.Namespace) -> None:
    conn = index.connect(args.db)
    article = Article(
        id=storage.generate_id(),
        title=args.title,
        media_type=args.media_type,
        summary=args.summary or "",
        tags=args.tags or [],
        references=args.reference or [],
        images=args.image or [],
        published_date=args.published_date or date.today().isoformat(),
        created_at=date.today().isoformat(),
        body=_read_body(args.body_file),
    )
    try:
        storage.write_article(args.articles_dir, article)
    except storage.ValidationError as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)
    index.upsert_article(conn, article)
    print(f"added {article.id}: {article.title} -> {article.file_path}")


def cmd_list(args: argparse.Namespace) -> None:
    conn = index.connect(args.db)
    _print_rows(index.list_all(conn))


def cmd_search(args: argparse.Namespace) -> None:
    conn = index.connect(args.db)
    _print_rows(index.search(conn, tag=args.tag, title=args.title))


def cmd_edit(args: argparse.Namespace) -> None:
    conn = index.connect(args.db)
    path = storage.article_path(args.articles_dir, args.id)
    if not path.exists():
        print(f"error: article {args.id} not found", file=sys.stderr)
        sys.exit(1)

    article = storage.read_article(path)
    if args.title is not None:
        article.title = args.title
    if args.media_type is not None:
        article.media_type = args.media_type
    if args.summary is not None:
        article.summary = args.summary
    if args.tags is not None:
        article.tags = args.tags
    if args.reference is not None:
        article.references = args.reference
    if args.image is not None:
        article.images = args.image
    if args.published_date is not None:
        article.published_date = args.published_date
    if args.body_file is not None:
        article.body = _read_body(args.body_file)

    try:
        storage.write_article(args.articles_dir, article)
    except storage.ValidationError as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)
    index.upsert_article(conn, article)
    print(f"updated {article.id}")


def cmd_delete(args: argparse.Namespace) -> None:
    conn = index.connect(args.db)
    path = storage.article_path(args.articles_dir, args.id)
    if not path.exists():
        print(f"error: article {args.id} not found", file=sys.stderr)
        sys.exit(1)
    storage.delete_article_file(args.articles_dir, args.id)
    index.delete_article(conn, args.id)
    print(f"deleted {args.id}")


def cmd_reindex(args: argparse.Namespace) -> None:
    conn = index.connect(args.db)
    count = index.rebuild_index(conn, args.articles_dir)
    print(f"reindexed {count} article(s)")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="article", description="Article Catalog System CLI")
    parser.add_argument("--articles-dir", dest="articles_dir", default=DEFAULT_ARTICLES_DIR)
    parser.add_argument("--db", default=DEFAULT_DB_PATH)
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="Add a new article")
    p_add.add_argument("--title", required=True)
    p_add.add_argument("--media-type", dest="media_type", required=True, choices=sorted(MEDIA_TYPES))
    p_add.add_argument("--summary")
    p_add.add_argument("--tag", dest="tags", action="append")
    p_add.add_argument("--reference", action="append")
    p_add.add_argument("--image", action="append")
    p_add.add_argument("--published-date", dest="published_date", help="Historical date for backfilled articles (YYYY-MM-DD)")
    p_add.add_argument("--body-file", dest="body_file", help="Path to a Markdown body file, or '-' for stdin")
    p_add.set_defaults(func=cmd_add)

    p_list = sub.add_parser("list", help="List all articles")
    p_list.set_defaults(func=cmd_list)

    p_search = sub.add_parser("search", help="Search articles by tag and/or title")
    p_search.add_argument("--tag")
    p_search.add_argument("--title")
    p_search.set_defaults(func=cmd_search)

    p_edit = sub.add_parser("edit", help="Edit an existing article")
    p_edit.add_argument("id")
    p_edit.add_argument("--title")
    p_edit.add_argument("--media-type", dest="media_type", choices=sorted(MEDIA_TYPES))
    p_edit.add_argument("--summary")
    p_edit.add_argument("--tag", dest="tags", action="append")
    p_edit.add_argument("--reference", action="append")
    p_edit.add_argument("--image", action="append")
    p_edit.add_argument("--published-date", dest="published_date")
    p_edit.add_argument("--body-file", dest="body_file")
    p_edit.set_defaults(func=cmd_edit)

    p_delete = sub.add_parser("delete", help="Delete an article")
    p_delete.add_argument("id")
    p_delete.set_defaults(func=cmd_delete)

    p_reindex = sub.add_parser("reindex", help="Rebuild the SQLite index from Markdown files (ADR-002)")
    p_reindex.set_defaults(func=cmd_reindex)

    return parser


def main(argv=None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
