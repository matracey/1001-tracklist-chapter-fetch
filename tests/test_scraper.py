"""
Tests for the scraper module.
"""

import unittest
from unittest.mock import MagicMock, patch

from scrapling.parser import Adaptor

from src.tracklist_chapter_fetch.scraper import ScrapingError, TracklistScraper


class TestScraper(unittest.TestCase):

    def setUp(self):
        """Set up for each test."""
        self.scraper = TracklistScraper()

        # Example HTML with a simple tracklist structure
        self.sample_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta property="og:title" content="Test Tracklist">
        </head>
        <body>
            <div class="tlpContainer">
                <div class="tlpItem">
                    <div class="tlpCuePointTimecode"><span class="tcWrap">0:34</span></div>
                    <div class="tlpTitleAndArtists">
                        <span class="blueTxt"><a>Artist1</a> & <a>Artist2</a></span>
                        <span class="trackValue">Track Title 1</span>
                    </div>
                </div>
                <div class="tlpItem">
                    <div class="tlpCuePointTimecode"><span class="tcWrap">3:53</span></div>
                    <div class="tlpTitleAndArtists">
                        <span class="blueTxt"><a>Artist3</a></span>
                        <span class="trackValue">Track Title 2</span>
                    </div>
                </div>
                <div class="tlpItem">
                    <div class="tlpCuePointTimecode"><span class="tcWrap">7:42</span></div>
                    <div class="tlpTitleAndArtists">
                        <span class="blueTxt"><a>Artist4</a></span>
                        <span class="trackValue">Track Title 3</span>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """

    @patch("src.tracklist_chapter_fetch.scraper.requests.get")
    def test_fetch_page(self, mock_requests_get):
        """Test fetching a page with mocked response."""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = self.sample_html

        # Setup mock requests.get
        mock_requests_get.return_value = mock_response

        # Test function
        result = self.scraper.fetch_page("https://www.1001tracklists.com/test")

        # Assertions
        self.assertIsInstance(result, Adaptor)
        mock_requests_get.assert_called_once()

    @patch("src.tracklist_chapter_fetch.scraper.requests.get")
    def test_fetch_page_error(self, mock_requests_get):
        """Test error handling when fetching fails."""
        # Setup mock response for error
        mock_response = MagicMock()
        mock_response.status_code = 404

        # Setup mock requests.get
        mock_requests_get.return_value = mock_response

        # Test function with exception
        with self.assertRaises(ScrapingError):
            self.scraper.fetch_page("https://www.1001tracklists.com/nonexistent")

    def test_parse_tracklist(self):
        """Test parsing a tracklist from HTML."""
        # Create a mock Adaptor object
        mock_adaptor = MagicMock(spec=Adaptor)
        mock_adaptor.body = self.sample_html

        # Mock container
        mock_container = MagicMock()

        # Mock track items
        mock_track_item1 = self.__create_mock_track_item__("0:34", "Track Title 1")
        mock_track_item2 = self.__create_mock_track_item__("3:53", "Track Title 2")
        mock_track_item3 = self.__create_mock_track_item__("7:42", "Track Title 3")

        # Mock meta title
        mock_title = MagicMock()
        mock_title.text = "Test Tracklist"
        mock_title.get.return_value = "Test Tracklist"

        # Set up mock returns
        mock_adaptor.css.side_effect = lambda selector: {
            ".tlpContainer": [mock_container],
            "meta[property='og:title']": [mock_title],
            "title": (
                [mock_title] if "meta[property='og:title']" not in selector else []
            ),
            ".tlpItem": [mock_track_item1, mock_track_item2, mock_track_item3],
        }.get(selector, [])

        mock_container.css.side_effect = lambda selector: {
            ".tlpItem": [mock_track_item1, mock_track_item2, mock_track_item3]
        }.get(selector, [])

        # Call the function
        tracks = self.scraper.parse_tracklist(mock_adaptor)

        # Check results
        self.assertEqual(len(tracks), 3)
        self.assertEqual(tracks[0]["title"], "Track Title 1")
        self.assertEqual(tracks[0]["timestamp"], "0:34")
        self.assertEqual(tracks[1]["title"], "Track Title 2")
        self.assertEqual(tracks[2]["timestamp"], "7:42")

    def __create_mock_track_item__(self, timestamp, title):
        """Helper to create mock track items for testing."""
        mock_item = MagicMock()

        # Mock timestamp element
        mock_timestamp_elem = MagicMock()
        mock_timestamp_elem.text = timestamp

        # Mock title element
        mock_title_elem = MagicMock()
        mock_title_elem.text = title

        # Configure mock item's css method to return different elements
        mock_item.css.side_effect = lambda selector: {
            ".tlpCuePointTimecode .tcWrap": [mock_timestamp_elem] if timestamp else [],
            ".trackValue": [mock_title_elem] if title else [],
        }.get(selector, [])

        return mock_item

    def test_parse_tracklist_empty(self):
        """Test error handling with invalid HTML."""
        # Setup mock adaptor that finds no tracklist
        mock_adaptor = MagicMock(spec=Adaptor)
        mock_adaptor.body = "<html><body>No tracklist here</body></html>"

        # No containers or items found
        mock_adaptor.css.return_value = []

        with self.assertRaises(ScrapingError):
            self.scraper.parse_tracklist(mock_adaptor)

    @patch.object(TracklistScraper, "fetch_page")
    @patch.object(TracklistScraper, "parse_tracklist")
    def test_get_tracklist(self, mock_parse, mock_fetch):
        """Test the full get_tracklist method with mocks."""
        # Setup mocks
        mock_adaptor = MagicMock(spec=Adaptor)
        mock_fetch.return_value = mock_adaptor
        mock_parse.return_value = [
            {"title": "Artist1 - Track1", "artist": None, "timestamp": "0:30"},
            {"title": "Artist2 - Track2", "artist": None, "timestamp": "3:45"},
        ]

        # Test function
        url = "https://www.1001tracklists.com/test"
        result = self.scraper.get_tracklist(url)

        # Assertions
        mock_fetch.assert_called_once_with(url)
        mock_parse.assert_called_once_with(mock_adaptor)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["title"], "Artist1 - Track1")
        self.assertEqual(result[1]["timestamp"], "3:45")


if __name__ == "__main__":
    unittest.main()
