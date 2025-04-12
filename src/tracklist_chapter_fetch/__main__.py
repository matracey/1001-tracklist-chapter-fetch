"""
Entry point module for running the package directly with Python.
"""
import sys
from .cli import main

if __name__ == "__main__":
    sys.exit(main())