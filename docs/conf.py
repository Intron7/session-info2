"""Configuration file for the Sphinx documentation builder."""

from __future__ import annotations

from functools import partial
from importlib.metadata import metadata
from importlib.util import find_spec
from subprocess import run

_sbc = (
    ["sphinx_build_compatibility.extension"]
    if find_spec("sphinx_build_compatibility")
    else []
)

_info = metadata("session_info2")

# specify project details
master_doc = "index"
project = _info.get("Name")

# basic build settings
html_theme = "furo"
extensions = ["myst_nb", *_sbc]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "**.ipynb_checkpoints"]
nitpicky = True
suppress_warnings = ["mystnb.unknown_mime_type"]

# myst_nb settings
nb_execution_mode = "force"
nb_execution_show_tb = True
# For debugging: nb_execution_timeout = -1


# https://github.com/executablebooks/MyST-NB/issues/574
def _patch_myst_nb() -> None:
    from jupyter_cache.executors import utils  # type: ignore[import-not-found]
    from myst_nb.core.execute import cache, direct  # type: ignore[import-not-found]

    run(  # noqa: S603
        ["hatch", "-v", "run", "notebook:install-kernel"],  # noqa: S607
        check=True,
    )

    cache.single_nb_execution = direct.single_nb_execution = partial(
        utils.single_nb_execution, kernel_name="session-info2"
    )


_patch_myst_nb()
