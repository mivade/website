import logging
from typing import Type

from tornado.web import RequestHandler

from .pages import Page

logger = logging.getLogger(__name__)


def make_handler(page: Page) -> Type:
    """Make a handler that can render a page."""

    class PageHandler(RequestHandler):
        def get(self):
            logger.info(f"Rendering {page.name}")
            markdown = page.to_html()
            # TODO: template rendering
            html = f"{markdown}"
            self.write(html)

    return PageHandler


class BlogIndexHandler(RequestHandler):
    """Render a page showing all blog entries."""

    def get(self):
        self.write("TODO: List of all blog entries")
