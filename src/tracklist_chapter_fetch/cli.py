"""
Command Line Interface for Tracklist Chapter Fetch.
"""

import argparse
import sys
import traceback
from typing import List, Optional

from .metadata import MetadataError, generate_ffmetadata, save_metadata_to_file
from .scraper import ScrapingError, TracklistScraper
from .utils import ValidationError, logger, setup_logging, validate_url


def parse_args(args: Optional[List[str]] = None) -> argparse.Namespace:
    """
    Parse command line arguments.

    Args:
        args: Command line arguments (defaults to sys.argv[1:])

    Returns:
        Parsed arguments as Namespace object
    """
    parser = argparse.ArgumentParser(
        description="Extract tracklist from 1001tracklists and convert to FFMETADATA format for chapter markers"
    )

    parser.add_argument("url", help="URL of the 1001tracklists page to extract")

    parser.add_argument(
        "-o",
        "--output",
        dest="output_file",
        default="output.ffmetadata",
        help="output file path (default: output.ffmetadata)",
    )

    parser.add_argument(
        "-q", "--quiet", action="store_true", help="suppress progress messages"
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="show detailed processing information",
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
        logger.info("Processing tracklist URL: %s", parsed_args.url)
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

        logger.info("Successfully processed %d tracks", len(tracks))
        return 0

    except ValidationError as e:
        logger.error("Validation error: %s", str(e))
        return 1
    except ScrapingError as e:
        logger.error("Scraping error: %s", str(e))
        return 2
    except MetadataError as e:
        logger.error("Metadata error: %s", str(e))
        return 3
    except (OSError, RuntimeError) as e:
        logger.error("Unexpected error: %s", str(e))
        if parsed_args.verbose:

            traceback.print_exc()
        return 4


if __name__ == "__main__":
    sys.exit(main())
