"""
FFMETADATA generation module for creating chapter metadata files.
"""

from typing import Any, Dict, List, Optional, Tuple

from .utils import format_time_ms, logger


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


def __get_track_timings__(
    track: Dict[str, Any], track_index: int, tracks: List[Dict[str, Any]]
) -> Optional[Tuple[int, int]]:
    """
    Get start and end times for a track in milliseconds.

    Args:
        track: Current track dictionary
        track_index: Index of current track in the tracks list
        tracks: Complete list of tracks

    Returns:
        Tuple of (start_ms, end_ms) or None if timing could not be determined
    """
    # Get timestamp and convert to milliseconds
    timestamp = track.get("timestamp")
    if not timestamp:
        logger.warning("Missing timestamp for track %d, skipping", track_index + 1)
        return None

    start_ms = format_time_ms(timestamp)
    if start_ms is None:
        logger.warning(
            "Invalid timestamp format for track %d: %s", track_index + 1, timestamp
        )
        return None

    # Calculate end time
    end_ms = None

    # If not the last track, use next track's start time as end time
    if track_index < len(tracks) - 1:
        next_timestamp = tracks[track_index + 1].get("timestamp")
        if next_timestamp:
            end_ms = format_time_ms(next_timestamp)

        # If we can't determine the end time, skip this track
        if end_ms is None:
            logger.warning(
                "Cannot determine end time for track %d, skipping", track_index + 1
            )
            return None

    # For the last track, use a default duration
    if end_ms is None:
        logger.warning(
            "Last track (%d) has no end time. Using a default duration.",
            track_index + 1,
        )
        # Default to 4 minutes for the last track
        end_ms = start_ms + (4 * 60 * 1000)

    return start_ms, end_ms


def __format_chapter_title__(track: Dict[str, Any]) -> str:
    """
    Format the chapter title from track information.

    Args:
        track: Track dictionary with 'artist' and 'title' fields

    Returns:
        Formatted chapter title string
    """
    title = track.get("title", "Unknown Title")
    artist = track.get("artist")

    if artist:
        return f"{artist} - {title}"
    return title
