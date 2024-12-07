"""Init file for colortext package.

This file is used to define the package's public API.

The public API consists of the following functions:
- print_color_text: A function to print colored text to the console.
- color_text: A decorator to return colored text.

The __version__ variable is also defined in this file.
"""

import importlib.metadata
from .stringstyler import print_styler, text_styler  # noqa: F401
# noqa: F401 is used to ignore flake8, ruff... warning for unused import


# get version from pyproject.toml / stringstyler is the package name
__version__ = importlib.metadata.version("stringstyler")
