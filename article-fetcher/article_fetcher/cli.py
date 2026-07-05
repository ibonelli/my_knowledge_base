import argparse
import sys
from datetime import date
from pathlib import Path

from . import editor, extract, frontmatter, pipeline, render
from .fetcher import FetchError


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="article-fetch",
        description="Fetch a URL, convert it to Markdown, and stage it for review as a front-matter file.",
    )
    parser.add_argument("url")
    parser.add_argument(
        "--media-type",
        dest="media_type",
        default=frontmatter.DEFAULT_MEDIA_TYPE,
        choices=sorted(frontmatter.MEDIA_TYPES),
    )
    parser.add_argument("--tag", dest="tags", action="append", default=[])
    parser.add_argument("--output-dir", dest="output_dir", default="imported")
    parser.add_argument(
        "--no-playwright-fallback",
        dest="allow_playwright_fallback",
        action="store_false",
    )
    parser.add_argument("--timeout", type=float, default=15.0)
    parser.add_argument("--yes", "-y", dest="skip_confirm", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        extracted = pipeline.fetch_and_extract(
            args.url,
            allow_playwright_fallback=args.allow_playwright_fallback,
            timeout=args.timeout,
        )
    except (FetchError, render.RenderError, extract.ExtractionError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)

    article_id = frontmatter.generate_id()
    today = date.today().isoformat()
    output_path = Path(args.output_dir) / f"{article_id}.md"

    front_matter = frontmatter.build_front_matter(
        article_id=article_id,
        title=extracted.title or args.url,
        summary="",
        media_type=args.media_type,
        tags=args.tags,
        references=[args.url],
        images=[],
        published_date=extracted.published_date or today,
        created_at=today,
    )
    draft = frontmatter.render_markdown(front_matter, extracted.body_markdown)

    if extracted.word_count < pipeline.MIN_WORD_COUNT and not extracted.used_fallback:
        print(
            f"warning: extracted content is thin ({extracted.word_count} words) "
            "and the Playwright fallback was not used or disabled; review carefully",
            file=sys.stderr,
        )

    edited_text = editor.edit_in_editor(draft)

    try:
        meta, body = frontmatter.parse_markdown(edited_text)
        frontmatter.validate_front_matter(meta)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)

    if not args.skip_confirm and not editor.confirm(f"Save to {output_path}?"):
        print("aborted, nothing saved")
        return

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(edited_text, encoding="utf-8")
    print(f"saved {meta.get('id', article_id)} -> {output_path}")


if __name__ == "__main__":
    main()
