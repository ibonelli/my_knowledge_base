from dataclasses import dataclass, field

MEDIA_TYPES = {"written", "graphic", "video"}


@dataclass
class Article:
    id: str
    title: str
    media_type: str
    summary: str = ""
    tags: list[str] = field(default_factory=list)
    references: list[str] = field(default_factory=list)
    images: list[str] = field(default_factory=list)
    published_date: str | None = None
    created_at: str | None = None
    body: str = ""
    file_path: str | None = None
