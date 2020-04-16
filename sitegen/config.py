import dataclasses as dc
import os


@dc.dataclass
class Config:
    root: str = dc.field(
        default_factory=lambda: os.path.join(os.getcwd(), "content"),
        metadata={"help": "root content directory"},
    )
    port: int = dc.field(default=9000, metadata={"help": "port to serve on"})
    # FIXME: make debug False by default
    debug: bool = dc.field(default=True, metadata={"help": "enable debug mode"})


config = Config()
