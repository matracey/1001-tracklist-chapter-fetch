"""
Utility functions for Tracklist Chapter Fetch.
"""
import re
import sys
import logging
from typing import Optional, Any, Dict
from urllib.parse import urlparse

# Configure logging
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(levelname)s: %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


class ValidationError(Exception):
    """Exception raised for validation errors."""
    pass


def validate_url(url: str) -> bool:
    """
    Validate that a given string is a valid 1001tracklists.com URL.
    
    Args:
        url: The URL string to validate
        
    Returns:
        True if the URL is valid, False otherwise
        
    Raises:
        ValidationError: If URL validation fails
    """
    if not url:
        raise ValidationError("URL cannot be empty")
    
    try:
        result = urlparse(url)
        is_valid = all([result.scheme, result.netloc])
        is_1001tracklists = "1001tracklists.com" in result.netloc
        
        if not is_valid:
            raise ValidationError("Invalid URL format")
        if not is_1001tracklists:
            raise ValidationError("URL must be from 1001tracklists.com domain")
            
        return True
    except Exception as e:
        raise ValidationError(f"URL validation error: {str(e)}")


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


def format_time_ms(time_str: str) -> Optional[int]:
    """
    Convert time string (MM:SS) to milliseconds.
    
    Args:
        time_str: Time string in MM:SS format
        
    Returns:
        Time in milliseconds or None if conversion fails
    """
    try:
        # Handle various time formats
        if ":" in time_str:
            parts = time_str.split(":")
            if len(parts) == 2:  # MM:SS
                minutes, seconds = map(int, parts)
                return (minutes * 60 + seconds) * 1000
            elif len(parts) == 3:  # HH:MM:SS
                hours, minutes, seconds = map(int, parts)
                return (hours * 3600 + minutes * 60 + seconds) * 1000
        else:
            # Try direct conversion for seconds only
            return int(time_str) * 1000
            
    except (ValueError, TypeError) as e:
        logger.warning(f"Failed to convert time '{time_str}': {str(e)}")
        return None