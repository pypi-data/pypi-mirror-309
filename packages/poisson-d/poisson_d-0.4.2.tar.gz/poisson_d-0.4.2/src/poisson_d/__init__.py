"""Top-level package for poisson_d."""

import toml


def load_version():
    config = toml.load("pyproject.toml")
    return config["project"]["version"]


__author__ = """Qi HU"""
__email__ = "hu.verrerie@gmail.com"
__version__ = load_version()
