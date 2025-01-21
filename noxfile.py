import nox


@nox.session(venv_backend="none")
def build(session: nox.Session) -> None:
    """Build the site."""
    session.run("git", "submodule", "update", "--init", external=True)

    with session.cd("mivade.github.io"):
        session.run("git", "switch", "main")

    session.run("quarto", "render", "src", external=True)
