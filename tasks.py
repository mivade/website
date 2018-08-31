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


def metadata_to_dataframe(metadata: str) -> pd.DataFrame:
    """Convert JSON-encoded blog metadata into a DataFrame."""
    metadata = json.loads(metadata)
    paths = list(metadata.keys())
    df = pd.DataFrame({
        "path": paths,
        "title": [metadata[key]["title"] for key in paths],
        "date": [metadata[key]["date"] for key in paths],
    }).sort_values(by="date", ascending=False)
    return df


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
def archive_page(ctx):
    """Create or update the page that lists all blog entries."""
    metadata = metadata_to_dataframe(ctx["blog_meta"])

    with open(Path().joinpath("content", "archives.md"), "w") as outfile:
        output = ["# Archives\n\n"]
        for _, row in metadata.iterrows():
            path = row["path"].replace("content/", "")
            date = (
                datetime.datetime
                .strptime(row["date"], "%Y-%m-%d")
                .strftime("%Y-%m-%d")
            )
            output.append(f'* <span align="right">{date}</span>&nbsp;&nbsp;'
                          f'[{row["title"]}]({path})\n')

        outfile.writelines(output)


@task(pre=[archive_page])
def mkdocs_yml(ctx):
    """Regenerate the mkdocs.yml file."""
    df = metadata_to_dataframe(ctx["blog_meta"])

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
    """Run the development server."""
    ctx.run(f"mkdocs serve -a localhost:{port}")


@task(pre=[mkdocs_yml])
def build(ctx):
    """Build the site."""
    ctx.run("mkdocs build")
