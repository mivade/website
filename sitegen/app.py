import logging

from tornado.ioloop import IOLoop
from tornado.web import Application

from .config import config
from .handlers import PageHandler, BlogIndexHandler
from .pages import get_all_pages

logger = logging.getLogger(__name__)


class _Application(Application):
    def __init__(self):
        pages = get_all_pages()
        handlers = [("/blog", BlogIndexHandler, {"pages": pages})]

        for name, document in pages.documents.items():
            route = "/" if name == "index" else "/{name}"
            handlers.append((route, PageHandler, {"page": document}))

        for name, entry in pages.entries.items():
            handlers.append((f"/blog/{name}\\.html", PageHandler, {"page": entry}))

        super().__init__(
            handlers, template_path=config.template_dir, debug=config.debug
        )


def main():
    logging.basicConfig(level=(logging.DEBUG if config.debug else logging.INFO))
    app = _Application()
    app.listen(config.port)
    logger.info(f"Listening on port {config.port}")
    IOLoop.current().start()


if __name__ == "__main__":
    main()
