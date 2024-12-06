"""
Aitronos Package

This package provides an API client for interacting with the Freddy Core API.
"""

# Import necessary classes and functions from the module
from .module import Aitronos

# Optional: You can add a version number for your package
__version__ = "0.1.3"

# You can make some of the classes or functions available at the package level
# This way users can do:
# from Aitronos import Aitronos
__all__ = ["Aitronos"]
