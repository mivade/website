import logging

from tornado.ioloop import IOLoop
from tornado.web import Application

from .config import config
from .handlers import BaseHandler

logger = logging.getLogger(__name__)


def main():
    logging.basicConfig(level=(logging.DEBUG if config.debug else logging.INFO))

    handlers = [(handler.route, handler) for handler in BaseHandler.subclasses]
    app = Application(handlers, debug=config.debug)
    app.listen(config.port)
    logger.debug(f"Handlers: {handlers}")
    logger.info(f"Listening on port {config.port}")
    IOLoop.current().start()


if __name__ == "__main__":
    main()
