from dataclasses import dataclass
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any, Dict

from .config import config
from .renderer import Renderer


@dataclass
class Page:
    """Base class for all page types."""

    source: Path

    def __post_init__(self):
        mtime = self.source.stat().st_mtime
        self.timestamp = datetime.fromtimestamp(mtime, tz=timezone.utc)
        self.renderer = Renderer()

    @property
    def name(self) -> str:
        return self.source.stem

    @property
    def metadata(self) -> Dict[str, Any]:
        self.to_html()  # have to do this to populate the ``Meta`` attribute
        return self.renderer.Meta

    @property
    def date(self) -> date:
        return datetime.strptime(self.metadata["date"][0], "%Y-%m-%d").date()

    def to_html(self) -> str:
        """Render the page as HTML."""
        return self.renderer.convert(self.source.read_text())


class Document(Page):
    """A page that is not a blog entry, e.g. a landing page or about page."""


class Entry(Page):
    """A page that is a blog entry."""


@dataclass
class PageIndex:
    """A container holding all pages.

    We use the following terminology:

    * page - any output
    * entry - a blog entry
    * document - non-blog pages e.g. landing page, about page, etc.

    """

    documents: Dict[str, Document]
    entries: Dict[str, Entry]


def get_all_pages() -> PageIndex:
    """Scan the root directory for pages."""

    root = Path(config.root)
    documents = {path.stem: Document(path) for path in root.glob("*.md")}
    entries = {path.stem: Entry(path) for path in config.blog_root.glob("*.md")}
    return PageIndex(documents, entries)
