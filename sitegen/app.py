import logging

from tornado.ioloop import IOLoop
from tornado.web import Application

from .config import config
from .handlers import BaseHandler
from .pages import get_all_pages

logger = logging.getLogger(__name__)


class _Application(Application):
    def __init__(self):
        handlers = [(handler.route, handler) for handler in BaseHandler.subclasses]
        handler_string = "\n".join(
            [
                f"{handler.route}\t{handler.__class__}"
                for handler in BaseHandler.subclasses
            ]
        )
        logger.debug(f"Handlers: {handler_string}")
        super().__init__(handlers, debug=config.debug)
        self.pages = get_all_pages()


def main():
    logging.basicConfig(level=(logging.DEBUG if config.debug else logging.INFO))
    app = _Application()
    app.listen(config.port)
    logger.info(f"Listening on port {config.port}")
    IOLoop.current().start()


if __name__ == "__main__":
    main()
