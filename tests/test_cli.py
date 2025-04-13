"""
Tests for the command-line interface module.
"""

import unittest

from src.tracklist_chapter_fetch.cli import parse_args


class TestCLI(unittest.TestCase):
    def test_parse_args_minimal(self):
        """Test argument parsing with just a URL."""
        args = parse_args(["https://www.1001tracklists.com/test"])
        self.assertEqual(args.url, "https://www.1001tracklists.com/test")
        self.assertEqual(args.output_file, "output.ffmetadata")
        self.assertFalse(args.quiet)
        self.assertFalse(args.verbose)


if __name__ == "__main__":
    unittest.main()
