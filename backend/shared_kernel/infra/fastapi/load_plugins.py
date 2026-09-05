"""Define the Load Plugins module for FastAPI."""

import importlib
import os


def load_plugins():
    """Load plugins for FastAPI."""
    # Implement plugin loading logic here
    plugins_dir = "./bootstrap/plugins"

    if not os.path.exists(plugins_dir):
        return

    for file_name in os.listdir(plugins_dir):
        if file_name.endswith(".py") and file_name != "__init__.py":
            module_name = file_name[:-3]  # Remove the .py extension
            module_path = f"bootstrap.plugins.{module_name}"

            importlib.import_module(module_path)
