"""
A module for project documentation tasks.
"""

# built-in
from pathlib import Path

# third-party
from vcorelib.paths import find_file
from vcorelib.task import Inbox, Outbox
from vcorelib.task.subprocess.run import SubprocessLogMixin

# internal
from experimental_lowqa import PKG_NAME
from experimental_lowqa.tasks.python import to_slug


class SphinxTask(SubprocessLogMixin):
    """A class to facilitate generating documentation with sphinx."""

    default_requirements = {
        "venv",
        "python-install-sphinx",
        "python-install-sphinx-book-theme",
        "python-editable",
    }

    async def run(self, inbox: Inbox, outbox: Outbox, *args, **kwargs) -> bool:
        """Generate ninja configuration files."""

        cwd: Path = args[0]
        project: str = args[1]

        venv_bin = inbox["venv"]["venv{python_version}"]["bin"]

        # Find templates directory.
        templates = find_file(
            "templates",
            package=to_slug(PKG_NAME),
            strict=True,
            logger=self.logger,
        )
        assert templates is not None

        # Generate sources with apidoc.
        result = await self.shell_cmd_in_dir(
            cwd.joinpath("docs"),
            [
                str(venv_bin.joinpath("sphinx-apidoc")),
                str(Path("..", project.replace("-", "_"))),
                "-t",
                str(templates),
                "-A",
                f"\"{kwargs.get('author', 'Libre Embedded')}\"",
                "-f",
                "-F",
                "-o",
                ".",
            ],
        )

        # Build.
        if result:
            result = await self.shell_cmd_in_dir(
                cwd.joinpath("docs"),
                [
                    str(venv_bin.joinpath("sphinx-build")),
                    "-W",
                    ".",
                    "_build",
                ],
            )

        return result
