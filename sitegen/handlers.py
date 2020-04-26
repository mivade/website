import logging

from tornado.web import RequestHandler

from .pages import Document, Entry, Page, PageIndex

logger = logging.getLogger(__name__)


class BaseHandler(RequestHandler):
    def path_for(self, page: Page) -> str:
        """Get the URL path for a page."""
        suffix = page.source.name.replace(".md", ".html")

        if isinstance(page, Document):
            return f"/{suffix}"
        elif isinstance(page, Entry):
            return f"/blog/{suffix}"
        else:
            raise ValueError("Invalid page type")


class PageHandler(BaseHandler):
    """Handler for all documents and blog entries."""

    def initialize(self, page: Page):
        self.page = page

    def get(self):
        logger.info(f"Rendering {self.page.name}")
        markdown = self.page.to_html()
        # TODO: template rendering
        html = f"{markdown}"
        self.write(html)


class BlogIndexHandler(BaseHandler):
    """Render a page showing all blog entries."""

    def initialize(self, pages: PageIndex):
        self.pages = pages

    def get(self):
        for key, entry in self.pages.entries.items():
            link = self.path_for(entry)
            self.write(f'<p><a href="{link}">{entry.name}</a></p>')
