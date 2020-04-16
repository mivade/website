import logging
from pathlib import Path
from typing import List

from tornado.web import RequestHandler

from .config import config
from .renderer import Renderer

logger = logging.getLogger(__name__)


class BaseHandler(RequestHandler):
    route: str
    subclasses: List["BaseHandler"] = []

    def __init_subclass__(cls, **kwargs):
        if cls not in BaseHandler.subclasses:
            BaseHandler.subclasses.append(cls)

    def get_path(self, name: str) -> Path:
        raise NotImplementedError

    def render_markdown(self, path: Path) -> str:
        """Read a markdown file and render it."""
        text = path.read_text()
        logger.info(f"Rendering {path}")
        html = Renderer.instance().convert(text)
        return html

    def get(self, name: str):  # FIXME: need to not pass in name directly
        path = self.get_path(name)
        html = self.render_markdown(path)
        self.write(html)


class IndexHandler(BaseHandler):
    """Handle the landing page."""

    route = r"/"

    def get_path(self, name):
        return Path(config.root, "index.md")


class PageHandler(BaseHandler):
    """Handle fixed, non-blog pages."""

    route = r"/(.*)"

    def get_path(self, name):
        return Path(config.root, f"{name}.md")


class BlogHandler(BaseHandler):
    """Handle blog pages."""

    route = r"/blog/(.*)"

    def get_path(self, name):
        return Path(config.root, "blog", f"{name}.md")
