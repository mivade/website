import asyncio
from pathlib import Path

from tornado.log import enable_pretty_logging
from tornado.web import Application, RequestHandler

SOURCE_DIR = Path(__file__).parent / "src"


class PageHandler(RequestHandler):
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
            # TODO: transform Markdown
            # TODO: render template
            self.write(path.read_bytes())


async def main() -> None:
    """Run the development server."""
    enable_pretty_logging()
    app = Application([("(.*)", PageHandler)], debug=True)
    app.listen(4444, "127.0.0.1")
    await asyncio.Event().wait()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
