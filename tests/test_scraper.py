"""
Tests for the scraper module.
"""

import unittest
from unittest.mock import MagicMock, patch

from scrapling.parser import Adaptor

from src.tracklist_chapter_fetch.scraper import TracklistScraper


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


if __name__ == "__main__":
    unittest.main()
