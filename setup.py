# =====================================
# generator=datazen
# version=3.2.0
# hash=29f345c5b752a50f363dcc12bf1d0576
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
    "name": "Vaughn Kottler",
    "email": "vaughn@libre-embedded.com",
    "username": "vkottler",
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
