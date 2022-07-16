import asyncio
from pathlib import Path

from markdown import Markdown

from tornado.log import enable_pretty_logging
from tornado.web import Application, RequestHandler, RedirectHandler, StaticFileHandler

SOURCE_DIR = Path(__file__).parent / "src"


class MarkdownHandler(RequestHandler):
    def initialize(self, markdown: Markdown) -> None:
        self.markdown = markdown

    def get(self, path: str) -> None:
        """Translate the input path into a filesystem path; find and write the
        file, rendering Markdown.

        """
        path = path.lstrip("/")
        filename = path.replace(".html", ".md")
        self._render_markdown(filename)

    def _render_markdown(self, filename: str) -> None:
        """Render the markdown file ``filename``."""
        path = SOURCE_DIR / filename

        if not path.is_file():
            self.send_error(404)
        else:
            # TODO: render template
            html = self.markdown.convert(path.read_text())
            self.write(html)


async def main() -> None:
    """Run the development server."""
    markdown = Markdown(
        extensions=["extra", "codehilite", "meta"], output_format="html5"
    )
    enable_pretty_logging()
    app = Application(
        [
            ("/", MarkdownHandler),
            (r"/(.*\.html)", MarkdownHandler, {"markdown": markdown}),
            ("/(.*)/", RedirectHandler, {"url": "{0}/index.html"}),
            ("/.+", StaticFileHandler, {"path": "src"}),
        ],
        debug=True,
    )
    app.listen(4444, "127.0.0.1")
    await asyncio.Event().wait()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
