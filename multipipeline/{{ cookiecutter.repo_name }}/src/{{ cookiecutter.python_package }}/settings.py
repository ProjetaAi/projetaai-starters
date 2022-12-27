"""Project settings.

There is no need to edit this file unless you want to
change values from the Kedro defaults. For further information, including these
default values, see
https://kedro.readthedocs.io/en/stable/kedro_project_setup/settings.html.
"""
import os


# Class that manages how configuration is loaded.
from kedro.config import TemplatedConfigLoader

CONFIG_LOADER_CLASS = TemplatedConfigLoader
# Keyword arguments to pass to the `CONFIG_LOADER_CLASS` constructor.
CONFIG_LOADER_ARGS = {"globals_pattern": "*globals.yml", "globals_dict": os.environ}

