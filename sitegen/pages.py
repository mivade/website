from dataclasses import dataclass
from pathlib import Path
from typing import Dict

from .config import config
from .renderer import Renderer


@dataclass
class Page:
    """Base class for all page types."""

    source: Path

    @property
    def name(self) -> str:
        return self.source.stem

    def to_html(self) -> str:
        """Render the page as HTML."""
        return Renderer.instance().convert(self.source.read_text())


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
