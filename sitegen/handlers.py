import logging
from pathlib import Path
from typing import List

from tornado.web import RequestHandler

from .config import config
from .pages import Page, PageIndex, get_all_pages
from .renderer import Renderer

logger = logging.getLogger(__name__)


class BaseHandler(RequestHandler):
    """Base handler class."""
    route: str
    subclasses: List["BaseHandler"] = []
    pages: PageIndex

    def __init_subclass__(cls, **kwargs):
        if cls not in BaseHandler.subclasses:
            BaseHandler.subclasses.append(cls)

    def get_page(self, *args) -> Page:
        raise NotImplementedError

    def render_markdown(self, page: Page) -> str:
        """Read a markdown file and render it."""
        logger.info(f"Rendering {page.name}")
        html = page.to_html()
        return html

    def prepare(self):
        self.pages = get_all_pages()
        logger.debug(self.pages)
        logger.debug("%r", dir(Renderer.instance()))

    def get(self, *args):
        page = self.get_page(*args)
        # TODO: implement templates and add rendered markdown to base
        html = f"{page.to_html()}"
        self.write(html)


class IndexHandler(BaseHandler):
    """Handle the landing page."""

    route = r"/"

    def get_page(self):
        return self.pages.documents["index"]


# FIXME: rename to DocumentHandler
class PageHandler(BaseHandler):
    """Handle fixed, non-blog pages."""

    route = r"/(.*)"

    def get_page(self, name):
        return self.pages.documents[name]


class BlogHandler(BaseHandler):
    """Handle blog pages."""

    route = r"/blog/(.*)"

    def get_page(self, name):
        return self.pages.blog[name]
