import logging
from typing import List

from tornado.web import RequestHandler

from .pages import Page, PageIndex

logger = logging.getLogger(__name__)

# TODO: rework so we have a function that constructs a handler; get list of pages
#       on app startup and generates all necessary handlers; this will get rid of
#       a bunch of regex corner cases


class BaseHandler(RequestHandler):
    """Base handler class."""

    route: str
    dynamic: bool = False
    subclasses: List["BaseHandler"] = []

    def __init_subclass__(cls, **kwargs):
        if cls not in BaseHandler.subclasses:
            BaseHandler.subclasses.append(cls)

    @property
    def pages(self) -> PageIndex:
        return self.application.pages

    def get_page(self, *args) -> Page:
        raise NotImplementedError

    def render_dynamic_content(self) -> str:
        """Render dynamic page content. Must be implemented when ``dynamic`` is
        set to ``True``.

        """
        raise NotImplementedError

    def render_markdown(self, page: Page) -> str:
        """Read a markdown file and render it."""
        logger.info(f"Rendering {page.name}")
        html = page.to_html()
        return html

    def get(self, *args):
        if not self.dynamic:
            page = self.get_page(*args)
            # TODO: implement templates and add rendered markdown to base
            html = f"{page.to_html()}"
            self.write(html)
        else:
            self.write(self.render_dynamic_content)


class IndexHandler(BaseHandler):
    """Handle the landing page."""

    route = r"/"

    def get_page(self):
        return self.pages.documents["index"]


class DocumentHandler(BaseHandler):
    """Handle documents."""

    # FIXME: needs to exclude /blog
    route = r"/(.*)"

    def get_page(self, name):
        return self.pages.documents[name]


class BlogIndexHandler(BaseHandler):
    """Render a page showing all blog entries."""

    route = r"/blog"
    dynamic = True

    def render_dynamic_content(self):
        # TODO: implement template rendering
        return "\n".join([entry.name for entry in self.pages.entries])


class BlogHandler(BaseHandler):
    """Handle blog pages."""

    route = r"/blog/(.*)"

    def get_page(self, name):
        return self.pages.blog[name]
