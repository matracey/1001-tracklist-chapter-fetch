"""
Tests for the command-line interface module.
"""

import unittest
from unittest.mock import MagicMock, patch

from src.tracklist_chapter_fetch.cli import main, parse_args
from src.tracklist_chapter_fetch.metadata import MetadataError
from src.tracklist_chapter_fetch.scraper import ScrapingError
from src.tracklist_chapter_fetch.utils import ValidationError


class TestCLI(unittest.TestCase):
    def test_parse_args_minimal(self):
        """Test argument parsing with just a URL."""
        args = parse_args(["https://www.1001tracklists.com/test"])
        self.assertEqual(args.url, "https://www.1001tracklists.com/test")
        self.assertEqual(args.output_file, "output.ffmetadata")
        self.assertFalse(args.quiet)
        self.assertFalse(args.verbose)

    def test_parse_args_all_options(self):
        """Test argument parsing with all options specified."""
        args = parse_args(
            [
                "https://www.1001tracklists.com/test",
                "-o",
                "custom.ffmetadata",
                "-q",
                "-v",
            ]
        )
        self.assertEqual(args.url, "https://www.1001tracklists.com/test")
        self.assertEqual(args.output_file, "custom.ffmetadata")
        self.assertTrue(args.quiet)
        self.assertTrue(args.verbose)

    @patch("src.tracklist_chapter_fetch.cli.validate_url")
    @patch("src.tracklist_chapter_fetch.cli.TracklistScraper")
    @patch("src.tracklist_chapter_fetch.cli.generate_ffmetadata")
    @patch("src.tracklist_chapter_fetch.cli.save_metadata_to_file")
    def test_main_success_path(
        self, mock_save, mock_generate, mock_scraper, mock_validate
    ):
        """Test successful execution path."""
        # Setup mocks
        mock_validate.return_value = True

        mock_scraper_instance = MagicMock()
        mock_tracks = [
            {"artist": "Artist1", "title": "Title1", "timestamp": "0:34"},
            {"artist": "Artist2", "title": "Title2", "timestamp": "3:53"},
        ]
        mock_scraper_instance.get_tracklist.return_value = mock_tracks
        mock_scraper.return_value = mock_scraper_instance

        mock_metadata = ";FFMETADATA1\n[CHAPTER]..."
        mock_generate.return_value = mock_metadata

        # Run the main function
        result = main(["https://www.1001tracklists.com/test", "-o", "test.ffmetadata"])

        # Assertions
        self.assertEqual(result, 0)  # Should return success code
        mock_validate.assert_called_once()
        mock_scraper_instance.get_tracklist.assert_called_once()
        mock_generate.assert_called_once_with(mock_tracks)
        mock_save.assert_called_once_with(mock_metadata, "test.ffmetadata")

    @patch("src.tracklist_chapter_fetch.cli.validate_url")
    def test_main_validation_error(self, mock_validate):
        """Test handling of validation errors."""
        mock_validate.side_effect = ValidationError("Invalid URL")

        result = main(["http://invalid.url"])

        self.assertEqual(result, 1)  # Should return validation error code

    @patch("src.tracklist_chapter_fetch.cli.validate_url")
    @patch("src.tracklist_chapter_fetch.cli.TracklistScraper")
    def test_main_scraping_error(self, mock_scraper, mock_validate):
        """Test handling of scraping errors."""
        mock_validate.return_value = True

        mock_scraper_instance = MagicMock()
        mock_scraper_instance.get_tracklist.side_effect = ScrapingError(
            "Scraping failed"
        )
        mock_scraper.return_value = mock_scraper_instance

        result = main(["https://www.1001tracklists.com/test"])

        self.assertEqual(result, 2)  # Should return scraping error code

    @patch("src.tracklist_chapter_fetch.cli.validate_url")
    @patch("src.tracklist_chapter_fetch.cli.TracklistScraper")
    @patch("src.tracklist_chapter_fetch.cli.generate_ffmetadata")
    def test_main_metadata_error(self, mock_generate, mock_scraper, mock_validate):
        """Test handling of metadata generation errors."""
        mock_validate.return_value = True

        mock_scraper_instance = MagicMock()
        mock_tracks = [{"artist": "Artist1", "title": "Title1", "timestamp": "0:34"}]
        mock_scraper_instance.get_tracklist.return_value = mock_tracks
        mock_scraper.return_value = mock_scraper_instance

        mock_generate.side_effect = MetadataError("Metadata generation failed")

        result = main(["https://www.1001tracklists.com/test"])

        self.assertEqual(result, 3)  # Should return metadata error code


if __name__ == "__main__":
    unittest.main()
