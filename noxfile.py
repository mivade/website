import nox


@nox.session()
def build(session: nox.Session) -> None:
    """Build the site."""
    session.run("git", "submodule", "update", external=True)
    session.run("quarto", "render", "src", external=True)
