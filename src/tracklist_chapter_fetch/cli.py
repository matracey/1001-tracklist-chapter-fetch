"""
Command Line Interface for Tracklist Chapter Fetch.
"""
import sys
import os
import argparse
import logging
from typing import List, Optional

from .utils import validate_url, setup_logging, ValidationError, logger
from .scraper import TracklistScraper, ScrapingError
from .metadata import generate_ffmetadata, save_metadata_to_file, MetadataError

def parse_args(args: Optional[List[str]] = None) -> argparse.Namespace:
    """
    Parse command line arguments.
    
    Args:
        args: Command line arguments (defaults to sys.argv[1:])
        
    Returns:
        Parsed arguments as Namespace object
    """
    parser = argparse.ArgumentParser(
        description='Extract tracklist from 1001tracklists and convert to FFMETADATA format for chapter markers'
    )
    
    parser.add_argument(
        'url',
        help='URL of the 1001tracklists page to extract'
    )
    
    parser.add_argument(
        '-o', '--output',
        dest='output_file',
        default='output.ffmetadata',
        help='output file path (default: output.ffmetadata)'
    )
    
    parser.add_argument(
        '-q', '--quiet',
        action='store_true',
        help='suppress progress messages'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='show detailed processing information'
    )
    
    return parser.parse_args(args)

def main(args: Optional[List[str]] = None) -> int:
    """
    Main entry point for the application.
    
    Args:
        args: Command line arguments (defaults to sys.argv[1:])
        
    Returns:
        Exit code (0 for success, non-zero for errors)
    """
    parsed_args = parse_args(args)
    
    # Configure logging
    setup_logging(verbose=parsed_args.verbose, quiet=parsed_args.quiet)
    
    try:
        # Validate URL
        logger.info(f"Processing tracklist URL: {parsed_args.url}")
        validate_url(parsed_args.url)
        
        # Initialize scraper and fetch tracklist
        logger.info("Fetching tracklist data...")
        scraper = TracklistScraper()
        tracks = scraper.get_tracklist(parsed_args.url)
        
        # Generate metadata
        logger.info("Generating FFMETADATA...")
        metadata = generate_ffmetadata(tracks)
        
        # Save metadata to file
        save_metadata_to_file(metadata, parsed_args.output_file)
        
        logger.info(f"Successfully processed {len(tracks)} tracks")
        return 0
        
    except ValidationError as e:
        logger.error(f"Validation error: {str(e)}")
        return 1
    except ScrapingError as e:
        logger.error(f"Scraping error: {str(e)}")
        return 2
    except MetadataError as e:
        logger.error(f"Metadata error: {str(e)}")
        return 3
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        if parsed_args.verbose:
            import traceback
            traceback.print_exc()
        return 4

if __name__ == "__main__":
    sys.exit(main())