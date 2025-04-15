# =====================================
# generator=datazen
# version=3.2.1
# hash=df0668e3256561dddbd442ed36f45959
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
        "3.12",
        "3.13",
    ],
}
setup(
    pkg_info,
    author_info,
)
