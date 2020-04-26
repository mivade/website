from markdown import Markdown

from .config import config


class Renderer(Markdown):
    def __init__(self):
        super().__init__(extensions=config.markdown_extensions)
