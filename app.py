import argparse
import asyncio
from datetime import date
import itertools
import os
from pathlib import Path
import shutil
from typing import Any, NewType

from markdown import Markdown

from tornado.httpclient import AsyncHTTPClient
from tornado.log import enable_pretty_logging
from tornado.web import Application, RequestHandler, RedirectHandler, StaticFileHandler

DEFAULT_PORT = 4444
SOURCE_DIR = Path(__file__).parent / "src"

Link = NewType("Link", str)
BlogEntry = tuple[date, str, Link]


class BaseHandler(RequestHandler):
    def get_template_namespace(self) -> dict[str, Any]:
        namespace = super().get_template_namespace()
        namespace["pre_title"] = ""
        return namespace


class MarkdownHandler(BaseHandler):
    def initialize(self, markdown_kwargs: dict[str, Any]) -> None:
        self.markdown = Markdown(**markdown_kwargs)

    def get(self, path: str | None = None) -> None:
        """Translate the input path into a filesystem path; find and write the
        file, rendering Markdown.

        """
        if path is None:
            path = "index.html"

        path = path.lstrip("/")
        filename = path.replace(".html", ".md")
        self._render_markdown(filename)

    def _render_markdown(self, filename: str) -> None:
        """Render the markdown file ``filename``."""
        path = SOURCE_DIR / filename

        if not path.is_file():
            self.send_error(404)
        else:
            html = self.markdown.convert(path.read_text())
            title = self.markdown.Meta.get("title")
            pre_title = f"{title[0]} - " if title is not None else ""
            self.render(
                "markdown_page.html", html=html, title=title[0], pre_title=pre_title
            )


class BlogIndexHandler(BaseHandler):
    def initialize(self, markdown_kwargs: dict[str, Any], directory: str) -> None:
        self.markdown = Markdown(**markdown_kwargs)
        self.directory = SOURCE_DIR / directory

    def get(self) -> None:
        """Render an index of blog pages."""
        self.render(
            "blog_index.html", entries=self._get_entries(), pre_title="Articles - "
        )

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


async def serve(port: int | None = None) -> None:
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
            ("/", MarkdownHandler, {"markdown_kwargs": markdown_kwargs}),
            (r"/(.*\.html)", MarkdownHandler, {"markdown_kwargs": markdown_kwargs}),
            ("/(.*)/", RedirectHandler, {"url": "{0}/index.html"}),
            ("/(.+)", StaticFileHandler, {"path": "src"}),
        ],
        template_path="templates",
        debug=True,
    )
    app.listen(port or DEFAULT_PORT, "127.0.0.1")
    await asyncio.Event().wait()


async def generate(
    output_directory: str | os.PathLike | None = "build", port: int | None = None
) -> None:
    """Generate all static content."""
    port = port or DEFAULT_PORT
    serve_task = asyncio.create_task(serve(port))
    url_pattern = "http://localhost:{port}/{name}"
    src = Path("src")
    dest = Path(output_directory)
    shutil.rmtree(dest, ignore_errors=True)

    try:
        client = AsyncHTTPClient()

        for path in itertools.chain(src.glob("**/*.*"), [src / "blog" / "index.html"]):
            name = str(path.relative_to(src))
            outdir = dest.joinpath(path.relative_to(src).parent)
            outdir.mkdir(parents=True, exist_ok=True)

            if name.endswith(".md"):
                name = name.replace(".md", ".html")

            url = url_pattern.format(port=port, name=name)
            response = await client.fetch(url)

            with dest.joinpath(name).open("wb") as outfile:
                outfile.write(response.body)
    finally:
        serve_task.cancel()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", "-p", type=int, help="port to serve on")
    parser.add_argument(
        "command", choices=["serve", "generate"], help="command to execute"
    )
    args = parser.parse_args()

    if args.command == "serve":
        try:
            asyncio.run(serve(port=args.port))
        except KeyboardInterrupt:
            pass
    elif args.command == "generate":
        asyncio.run(generate(port=args.port))
    else:
        parser.print_usage()
        raise SystemExit()


if __name__ == "__main__":
    main()
