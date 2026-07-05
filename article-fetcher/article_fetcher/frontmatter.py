import re
import uuid

import yaml

# Mirrors article_catalog/models.py MEDIA_TYPES. Duplicated locally, not imported,
# to keep this tool fully decoupled from article_catalog's package/dependencies.
MEDIA_TYPES = {"written", "graphic", "video"}
DEFAULT_MEDIA_TYPE = "written"

FRONT_MATTER_RE = re.compile(r"^---\n(.*?)\n---\n?(.*)$", re.DOTALL)


def generate_id() -> str:
    return uuid.uuid4().hex[:8]


def build_front_matter(
    *,
    article_id: str,
    title: str,
    summary: str,
    media_type: str,
    tags: list[str],
    references: list[str],
    images: list[str],
    published_date: str,
    created_at: str,
) -> dict:
    return {
        "id": article_id,
        "title": title,
        "summary": summary,
        "media_type": media_type,
        "tags": tags,
        "references": references,
        "images": images,
        "published_date": published_date,
        "created_at": created_at,
    }


def render_markdown(front_matter: dict, body: str) -> str:
    return "---\n" + yaml.safe_dump(front_matter, sort_keys=False) + "---\n\n" + (body or "")


def parse_markdown(text: str) -> tuple[dict, str]:
    match = FRONT_MATTER_RE.match(text)
    if not match:
        raise ValueError("missing YAML front-matter (expected a leading '---' block)")
    meta = yaml.safe_load(match.group(1)) or {}
    return meta, match.group(2).lstrip("\n")


def validate_front_matter(meta: dict) -> None:
    if not (meta.get("title") or "").strip():
        raise ValueError("title is required")
    if meta.get("media_type") not in MEDIA_TYPES:
        raise ValueError(f"media_type must be one of {sorted(MEDIA_TYPES)}")
