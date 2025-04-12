"""
FFMETADATA generation module for creating chapter metadata files.
"""
import os
import logging
from typing import List, Dict, Any, Optional

from .utils import logger, format_time_ms

class MetadataError(Exception):
    """Exception raised for metadata generation errors."""
    pass

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
    if not tracks:
        raise MetadataError("Cannot generate metadata: No tracks provided")
        
    logger.debug(f"Generating metadata for {len(tracks)} tracks")
    
    # Start with FFMETADATA header
    metadata = [";FFMETADATA1"]
    
    # Process each track to create chapter entries
    for i, track in enumerate(tracks):
        try:
            # Get required track information
            title = track.get("title", "Unknown Title")
            timestamp = track.get("timestamp")
            
            if not timestamp:
                logger.warning(f"Missing timestamp for track {i+1}, skipping")
                continue
                
            # Convert timestamp to milliseconds
            start_ms = format_time_ms(timestamp)
            if start_ms is None:
                logger.warning(f"Invalid timestamp format for track {i+1}: {timestamp}")
                continue
            
            # Calculate end time (if this is the last track, we'll leave it None)
            end_ms = None
            if i < len(tracks) - 1:
                next_timestamp = tracks[i + 1].get("timestamp")
                if next_timestamp:
                    end_ms = format_time_ms(next_timestamp)
            
            # If we can't determine the end time, skip this track
            if end_ms is None and i < len(tracks) - 1:
                logger.warning(f"Cannot determine end time for track {i+1}, skipping")
                continue
                
            # For the last track, we might not have an end time
            # We could either skip it or use a default duration
            if end_ms is None:
                logger.warning(f"Last track ({i+1}) has no end time. Using a default duration.")
                # Default to 4 minutes for the last track if no end time is available
                end_ms = start_ms + (4 * 60 * 1000)
            
            # Add chapter metadata
            metadata.append("[CHAPTER]")
            metadata.append("TIMEBASE=1/1000")
            metadata.append(f"START={start_ms}")
            metadata.append(f"END={end_ms}")
            metadata.append(f"title={title}")
            
        except Exception as e:
            logger.warning(f"Error processing track {i+1}: {str(e)}")
    
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
        logger.debug(f"Saving metadata to {output_path}")
        
        # Create directory if it doesn't exist
        directory = os.path.dirname(output_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
            
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(metadata)
            
        logger.info(f"Successfully saved metadata to {output_path}")
        
    except OSError as e:
        raise MetadataError(f"Failed to save metadata file: {str(e)}")