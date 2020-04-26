from dataclasses import dataclass
import dataclasses as dc
import os
from pathlib import Path
from typing import List


@dataclass
class Config:
    root: str = dc.field(
        default_factory=lambda: os.path.join(os.getcwd(), "content"),
        metadata={"help": "root content directory"},
    )
    blog_directory: str = dc.field(
        default="blog",
        metadata={"help": "subdirectory of root which contains blog entries"},
    )
    port: int = dc.field(default=9000, metadata={"help": "port to serve on"})
    markdown_extensions: List[str] = dc.field(
        default_factory=lambda: ["extra", "meta", "toc"],
        metadata={"help": "list of Markdown extensions to use"},
    )
    # FIXME: make debug False by default
    debug: bool = dc.field(default=True, metadata={"help": "enable debug mode"})

    @property
    def blog_root(self) -> Path:
        """Get the blog root path."""
        return Path(self.root, self.blog_directory)


config = Config()
