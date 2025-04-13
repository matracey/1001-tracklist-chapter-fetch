"""
FFMETADATA generation module for creating chapter metadata files.
"""

from typing import Any, Dict, List

from .utils import logger


class MetadataError(Exception):
    """Exception raised for metadata generation errors."""


def __validate_tracks__(tracks: List[Dict[str, Any]]) -> None:
    """
    Validate that the tracks list is not empty.

    Args:
        tracks: List of track dictionaries

    Raises:
        MetadataError: If tracks list is empty
    """
    if not tracks:
        raise MetadataError("Cannot generate metadata: No tracks provided")

    logger.debug("Generating metadata for %d tracks", len(tracks))
