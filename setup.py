# =====================================
# generator=datazen
# version=3.2.3
# hash=e40f89b4f85b7b639d710842b400f8df
# =====================================

"""
experimental-lowqa - Package definition for distribution.
"""

# third-party
try:
    from setuptools_wrapper.setup import setup
except (ImportError, ModuleNotFoundError):
    from experimental_lowqa_bootstrap.setup import setup  # type: ignore

# internal
from experimental_lowqa import DESCRIPTION, PKG_NAME, VERSION

author_info = {
    "name": "Libre Embedded",
    "email": "vaughn@libre-embedded.com",
    "username": "libre-embedded",
}
pkg_info = {
    "name": PKG_NAME,
    "slug": PKG_NAME.replace("-", "_"),
    "version": VERSION,
    "description": DESCRIPTION,
    "versions": [
        "3.13",
        "3.14",
    ],
}
setup(
    pkg_info,
    author_info,
)
