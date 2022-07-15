import asyncio
from pathlib import Path

from markdown import Markdown

from tornado.log import enable_pretty_logging
from tornado.web import Application, RequestHandler

SOURCE_DIR = Path(__file__).parent / "src"


class PageHandler(RequestHandler):
    def initialize(self, markdown: Markdown) -> None:
        self.markdown = markdown

    def get(self, path: str) -> None:
        """Translate the input path into a filesystem path; find and write the
        file, rendering Markdown as appropriate.

        """
        if path.endswith("/"):
            path = f"{path}index.html"

        path = path.lstrip("/")

        if path.endswith(".html"):
            filename = path.replace(".html", ".md")
            self._render_markdown(filename)
        else:
            # TODO: guess content-type
            self.write(Path(SOURCE_DIR, path).read_bytes())

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
    # FIXME: update regex to only accept .html or ending in /,
    #        use static handler for everything else
    app = Application([("(.*)", PageHandler, {"markdown": markdown})], debug=True)
    app.listen(4444, "127.0.0.1")
    await asyncio.Event().wait()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
