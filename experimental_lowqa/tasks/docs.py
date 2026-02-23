"""
A module for project documentation tasks.
"""

# built-in
from pathlib import Path
from shutil import copyfile, copytree, rmtree

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
        "python-deps",
        "python-install-sphinx",
        "python-install-sphinx-book-theme",
        "python-install-myst-parser",
        "python-editable",
    }

    async def run(  # pylint: disable=too-many-locals
        self,
        inbox: Inbox,
        outbox: Outbox,
        *args,
        **kwargs,
    ) -> bool:
        """Generate ninja configuration files."""

        cwd: Path = args[0]
        project: str = args[1]
        slug = project.replace("-", "_")

        venv_bin = inbox["venv"]["venv{python_version}"]["bin"]

        # Find templates directory.
        templates = find_file(
            "templates",
            package=to_slug(PKG_NAME),
            strict=True,
            logger=self.logger,
        )
        assert templates is not None

        metadata_args = ["-A", f"\"{kwargs.get('author', 'Libre Embedded')}\""]
        metadata = kwargs.get("version")
        if metadata:
            metadata_args.extend(["-V", metadata])

        docs_base = cwd.joinpath("docs")

        # Generate sources with apidoc.
        result = await self.shell_cmd_in_dir(
            docs_base,
            [
                str(venv_bin.joinpath("sphinx-apidoc")),
                str(Path("..", slug)),
                "-t",
                str(templates),
            ]
            + metadata_args
            + ["-f", "-F", "-o", "."],
        )

        # Build.
        if result:
            # Update images.
            rmtree(docs_base.joinpath("im"), ignore_errors=True)
            copytree(cwd.joinpath("im"), docs_base.joinpath("im"))

            result = await self.shell_cmd_in_dir(
                docs_base,
                [
                    str(venv_bin.joinpath("sphinx-build")),
                    "-W",
                    ".",
                    "_build",
                ],
            )

        # Publish (to package).
        if result:
            dest_dir = cwd.joinpath(slug, "data", "docs")
            rmtree(dest_dir, ignore_errors=True)
            dest_dir.mkdir()

            for item in docs_base.joinpath("_build").iterdir():
                if item.name in {"_modules", "_static"}:
                    copytree(item, dest_dir.joinpath(item.name))
                elif item.suffix in {".html", ".js"}:
                    copyfile(item, dest_dir.joinpath(item.name))

        return result
