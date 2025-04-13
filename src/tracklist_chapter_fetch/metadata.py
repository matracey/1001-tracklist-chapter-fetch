"""
FFMETADATA generation module for creating chapter metadata files.
"""

import os
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


def __create_chapter_metadata__(start_ms: int, end_ms: int, title: str) -> List[str]:
    """
    Create metadata lines for a single chapter.

    Args:
        start_ms: Start time in milliseconds
        end_ms: End time in milliseconds
        title: Chapter title

    Returns:
        List of metadata strings for the chapter
    """
    return [
        "[CHAPTER]",
        "TIMEBASE=1/1000",
        f"START={start_ms}",
        f"END={end_ms}",
        f"title={title}",
    ]


def __process_track__(
    track: Dict[str, Any], track_index: int, tracks: List[Dict[str, Any]]
) -> Optional[List[str]]:
    """
    Process a single track and generate its chapter metadata.

    Args:
        track: Track dictionary
        track_index: Index of the track in the tracks list
        tracks: Complete list of tracks

    Returns:
        List of metadata strings for the track or None if track processing fails
    """
    try:
        # Get timing information
        timing_result = __get_track_timings__(track, track_index, tracks)
        if timing_result is None:
            return None

        start_ms, end_ms = timing_result

        # Format chapter title
        chapter_title = __format_chapter_title__(track)

        # Create chapter metadata
        return __create_chapter_metadata__(start_ms, end_ms, chapter_title)

    except KeyError as e:
        logger.warning("Missing key in track %d: %s", track_index + 1, str(e))
    except ValueError as e:
        logger.warning("Invalid value in track %d: %s", track_index + 1, str(e))
    except TypeError as e:
        logger.warning("Type error in track %d: %s", track_index + 1, str(e))

    return None


def generate_ffmetadata(tracks: List[Dict[str, Any]]) -> str:
    """
    Generate FFMETADATA format string from track list.

    Args:
        tracks: List of track dictionaries with 'artist', 'title', and 'timestamp' fields

    Returns:
        String in FFMETADATA format

    Raises:
        MetadataError: If metadata generation fails
    """
    __validate_tracks__(tracks)

    # Start with FFMETADATA header
    metadata = [";FFMETADATA1"]

    # Process each track to create chapter entries
    for i, track in enumerate(tracks):
        chapter_metadata = __process_track__(track, i, tracks)
        if chapter_metadata:
            metadata.extend(chapter_metadata)

    if len(metadata) <= 1:
        raise MetadataError("No valid chapters could be generated")

    return "\n".join(metadata)


def save_metadata_to_file(metadata: str, output_path: str) -> None:
    """
    Save metadata string to a file.

    Args:
        metadata: String in FFMETADATA format
        output_path: Path to save the metadata file

    Raises:
        MetadataError: If file write operation fails
    """
    try:
        logger.debug("Saving metadata to %s", output_path)

        # Create directory if it doesn't exist
        directory = os.path.dirname(output_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(metadata)

        logger.info("Successfully saved metadata to %s", output_path)

    except OSError as e:
        raise MetadataError(f"Failed to save metadata file: {str(e)}") from e
