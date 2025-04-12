"""
Command Line Interface for Tracklist Chapter Fetch.
"""

import argparse
import sys
import traceback
from typing import List, Optional

from .utils import logger, setup_logging


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
        return 0

    except (OSError, RuntimeError) as e:
        logger.error("Unexpected error: %s", str(e))
        if parsed_args.verbose:

            traceback.print_exc()
        return 4


if __name__ == "__main__":
    sys.exit(main())
