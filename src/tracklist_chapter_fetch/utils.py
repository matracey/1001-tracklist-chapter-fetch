"""
Utility functions for Tracklist Chapter Fetch.
"""

import logging

# Configure logging
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(levelname)s: %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


class ValidationError(Exception):
    """Exception raised for validation errors."""



def setup_logging(verbose: bool = False, quiet: bool = False) -> None:
    """
    Configure logging level based on command line arguments.

    Args:
        verbose: Set to True for verbose logging (DEBUG level)
        quiet: Set to True to suppress all but error messages
    """
    if quiet:
        logger.setLevel(logging.ERROR)
    elif verbose:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
