import datetime
import json
from pathlib import Path

from invoke import task
from jinja2 import Environment, FileSystemLoader
import pandas as pd
import yaml


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.date):
            return f"{o.year}-{o.month}-{o.day}"
        return super().default(o)


@task
def blog_meta(ctx):
    """Read all metadata from blog posts and add it to the context."""
    blog_root = Path("content/blog")
    files = blog_root.glob("*.md")
    meta = {}

    for filename in files:
        with open(filename, "r") as f:
            raw = f.read()

            # FIXME: figure out how to use the markdown API directly to extract
            #        metadata instead of using this fragile method
            metadata = yaml.load(raw.split("---\n")[1].strip())
            meta[str(filename)] = metadata

    ctx["blog_meta"] = json.dumps(meta, cls=JSONEncoder)


@task(pre=[blog_meta])
def mkdocs_yml(ctx):
    """Regenerate the mkdocs.yml file."""
    metadata = json.loads(ctx["blog_meta"])
    paths = list(metadata.keys())

    df = pd.DataFrame({
        "path": paths,
        "title": [metadata[key]["title"] for key in paths],
        "date": [metadata[key]["date"] for key in paths],
    })

    years = list(
        df.date.apply(lambda row: row.split("-")[0])
        .sort_values(ascending=False)
        .unique()
    )

    entries = {
        year: [
            (row["title"], row["path"].lstrip("content/"))
            for _, row in df[df.date.str.startswith(year)].iterrows()
        ]
        for year in years
    }

    env = Environment(
        loader=FileSystemLoader(".")
    )

    template = env.get_template("mkdocs.yml.in")
    with open("mkdocs.yml", "w") as outfile:
        outfile.write(template.render(years=years, entries=entries))


@task(pre=[mkdocs_yml])
def serve(ctx, port=8000):
    ctx.run(f"mkdocs serve -a localhost:{port}")


@task(pre=[mkdocs_yml])
def build(ctx):
    ctx.run("mkdocs build")
