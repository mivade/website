from markdown import Markdown

from .config import config


class Renderer(Markdown):
    _instance = None

    def __init__(self):
        super().__init__(extensions=config.markdown_extensions)

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()

        return cls._instance
