import re
import uuid
from pathlib import Path

import yaml

from .models import MEDIA_TYPES, Article

FRONT_MATTER_RE = re.compile(r"^---\n(.*?)\n---\n?(.*)$", re.DOTALL)


class ValidationError(ValueError):
    pass


def validate_article(title: str, media_type: str) -> None:
    if not title or not title.strip():
        raise ValidationError("title is required")
    if media_type not in MEDIA_TYPES:
        raise ValidationError(f"media_type must be one of {sorted(MEDIA_TYPES)}")


def normalize_tags(tags: list[str] | None) -> list[str]:
    normalized: list[str] = []
    for tag in tags or []:
        cleaned = tag.strip().lower()
        if cleaned and cleaned not in normalized:
            normalized.append(cleaned)
    return normalized


def generate_id() -> str:
    return uuid.uuid4().hex[:8]


def article_path(articles_dir, article_id: str) -> Path:
    return Path(articles_dir) / f"{article_id}.md"


def write_article(articles_dir, article: Article) -> Article:
    validate_article(article.title, article.media_type)
    article.tags = normalize_tags(article.tags)

    front_matter = {
        "id": article.id,
        "title": article.title,
        "summary": article.summary,
        "media_type": article.media_type,
        "tags": article.tags,
        "references": article.references,
        "images": article.images,
        "published_date": article.published_date,
        "created_at": article.created_at,
    }

    path = article_path(articles_dir, article.id)
    path.parent.mkdir(parents=True, exist_ok=True)
    content = "---\n" + yaml.safe_dump(front_matter, sort_keys=False) + "---\n\n" + (article.body or "")
    path.write_text(content, encoding="utf-8")

    article.file_path = str(path)
    return article


def read_article(path) -> Article:
    path = Path(path)
    text = path.read_text(encoding="utf-8")
    match = FRONT_MATTER_RE.match(text)
    if not match:
        raise ValidationError(f"{path} is missing YAML front-matter")

    meta = yaml.safe_load(match.group(1)) or {}
    body = match.group(2).lstrip("\n")

    return Article(
        id=meta.get("id") or path.stem,
        title=meta.get("title", ""),
        media_type=meta.get("media_type", ""),
        summary=meta.get("summary") or "",
        tags=meta.get("tags") or [],
        references=meta.get("references") or [],
        images=meta.get("images") or [],
        published_date=meta.get("published_date"),
        created_at=meta.get("created_at"),
        body=body,
        file_path=str(path),
    )


def delete_article_file(articles_dir, article_id: str) -> None:
    path = article_path(articles_dir, article_id)
    if path.exists():
        path.unlink()


def iter_article_files(articles_dir) -> list[Path]:
    directory = Path(articles_dir)
    if not directory.exists():
        return []
    return sorted(directory.glob("*.md"))
