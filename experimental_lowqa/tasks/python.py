"""
A module for Python-project task registration.
"""

# built-in
from copy import copy
from pathlib import Path

# third-party
from vcorelib.task import Inbox, Outbox

# internal
from experimental_lowqa.edit import GenerateTags


def to_slug(data: str) -> str:
    """Get a slug from a string."""
    return data.replace("-", "_")


class PythonTags(GenerateTags):
    """A class implementing a task for generating tags files."""

    languages = "Python"

    extra_source_candidates = [
        ("tasks",),
        ("tests",),
        (Path.home(), "src", "python", "cpython", "Lib"),
    ]

    async def run(self, inbox: Inbox, outbox: Outbox, *args, **kwargs) -> bool:
        """Generate a tags files."""

        root: Path = args[0]

        py_root = root.joinpath(to_slug(root.name))

        src = root.joinpath("src")
        if not src.exists() and py_root.is_dir():
            src.symlink_to(py_root, target_is_directory=True)

        self.extra_source_candidates = copy(type(self).extra_source_candidates)

        # Add extra source candidates for other Python projects.
        for candidate in [
            "vcorelib",
            "runtimepy",
            "svgen",
            "experimental-lowqa",
            "quasimoto",
            "gnomish-army-knife",
        ]:
            if root.name != candidate:
                self.extra_source_candidates.append(
                    ("..", candidate, to_slug(candidate))
                )

        return await super().run(inbox, outbox, *args, **kwargs)
