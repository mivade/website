from markdown import Markdown


class Renderer(Markdown):
    _instance = None

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()

        return cls._instance
