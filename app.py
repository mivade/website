import asyncio
from datetime import date
from pathlib import Path
from typing import Any, NewType

from markdown import Markdown

from tornado.log import enable_pretty_logging
from tornado.web import Application, RequestHandler, RedirectHandler, StaticFileHandler

SOURCE_DIR = Path(__file__).parent / "src"

Link = NewType("Link", str)
BlogEntry = tuple[date, str, Link]


class MarkdownHandler(RequestHandler):
    def initialize(self, markdown_kwargs: dict[str, Any]) -> None:
        self.markdown = Markdown(**markdown_kwargs)

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


class BlogIndexHandler(RequestHandler):
    def initialize(self, markdown_kwargs: dict[str, Any], directory: str) -> None:
        self.markdown = Markdown(**markdown_kwargs)
        self.directory = SOURCE_DIR / directory

    def get(self) -> None:
        """Render an index of blog pages."""
        self.render("blog_index.html", entries=self._get_entries())

    def _get_entries(self) -> list[BlogEntry]:
        entries: list[BlogEntry] = []

        for path in self.directory.glob("*.md"):
            self.markdown.convert(path.read_text())
            metadata: dict[str, list[str]] = self.markdown.Meta
            entries.append(
                (
                    date.fromisoformat(metadata["date"][0]),
                    metadata["title"][0],
                    f"{path.with_suffix('.html').name}",
                )
            )

        return sorted(entries, key=lambda entry: entry[0], reverse=True)


async def main() -> None:
    """Run the development server."""
    markdown_kwargs = {
        "extensions": ["extra", "codehilite", "meta"],
        "output_format": "html5",
    }
    enable_pretty_logging()
    app = Application(
        [
            (
                "/blog/index.html",
                BlogIndexHandler,
                {"markdown_kwargs": markdown_kwargs, "directory": "blog"},
            ),
            ("/", MarkdownHandler),
            (r"/(.*\.html)", MarkdownHandler, {"markdown_kwargs": markdown_kwargs}),
            ("/(.*)/", RedirectHandler, {"url": "{0}/index.html"}),
            ("/.+", StaticFileHandler, {"path": "src"}),
        ],
        template_path="templates",
        debug=True,
    )
    app.listen(4444, "127.0.0.1")
    await asyncio.Event().wait()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
