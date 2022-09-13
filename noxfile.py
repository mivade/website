import nox


@nox.session
def build(session: nox.Session) -> None:
    """Build the site."""
    session.install("-r", "requirements.txt")
    session.run("python", "app.py", "generate")


@nox.session
def publish(session: nox.Session) -> None:
    """Build and publish the site."""

    def shell(command: str, **kwargs) -> None:
        session.run("bash", "-c", command, external=True, **kwargs)

    session.install("-r", "requirements.txt")
    session.run("python", "app.py", "generate")
    shell("git submodule update --init")

    with session.chdir("mivade.github.io"):
        shell("git checkout main")
        shell("git pull")

    shell("cp -R $BUILD_DIR mivade.github.io/", env={"BUILD_DIR": "build/*"})

    with session.chdir("mivade.github.io"):
        shell("git add -A")
        shell('git commit -m "Update site"')
        # TODO: automatically push. For now we require manual pushes.
        # shell("git push")
