"""
Tests for the scraper module.
"""
import unittest
from unittest.mock import patch, MagicMock
from src.tracklist_chapter_fetch.scraper import TracklistScraper, ScrapingError


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
    
    @patch('requests.Session')
    def test_fetch_page(self, mock_session):
        """Test fetching a page with mocked response."""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = self.sample_html
        
        mock_session_instance = MagicMock()
        mock_session_instance.get.return_value = mock_response
        mock_session.return_value = mock_session_instance
        
        # Create a new scraper with mocked session
        scraper = TracklistScraper()
        scraper.session = mock_session_instance  # Use our mock session directly
        
        # Test function
        result = scraper.fetch_page("https://www.1001tracklists.com/test")
        
        # Assertions
        self.assertEqual(result, self.sample_html)
        mock_session_instance.get.assert_called_once()
    
    @patch('requests.Session')
    def test_fetch_page_error(self, mock_session):
        """Test error handling when fetching fails."""
        # Setup mock response for error
        mock_response = MagicMock()
        mock_response.status_code = 404
        
        mock_session_instance = MagicMock()
        mock_session_instance.get.return_value = mock_response
        mock_session.return_value = mock_session_instance
        
        # Create a new scraper with mocked session
        scraper = TracklistScraper()
        scraper.session = mock_session_instance
        
        # Test function with exception
        with self.assertRaises(ScrapingError):
            scraper.fetch_page("https://www.1001tracklists.com/nonexistent")
    
    def test_parse_tracklist(self):
        """Test parsing a tracklist from HTML."""
        tracks = self.scraper.parse_tracklist(self.sample_html)
        
        # Check that we got the expected number of tracks
        self.assertEqual(len(tracks), 3)
        
        # Check the content of the first track
        self.assertEqual(tracks[0]["artist"], "Artist1 & Artist2")
        self.assertEqual(tracks[0]["title"], "Track Title 1")
        self.assertEqual(tracks[0]["timestamp"], "0:34")
        
        # Check the content of the second track
        self.assertEqual(tracks[1]["artist"], "Artist3")
        self.assertEqual(tracks[1]["title"], "Track Title 2")
        self.assertEqual(tracks[1]["timestamp"], "3:53")
    
    def test_parse_tracklist_empty(self):
        """Test error handling with invalid HTML."""
        invalid_html = "<html><body>No tracklist here</body></html>"
        
        with self.assertRaises(ScrapingError):
            self.scraper.parse_tracklist(invalid_html)
    
    @patch.object(TracklistScraper, 'fetch_page')
    @patch.object(TracklistScraper, 'parse_tracklist')
    def test_get_tracklist(self, mock_parse, mock_fetch):
        """Test the full get_tracklist method with mocks."""
        # Setup mocks
        mock_fetch.return_value = self.sample_html
        mock_parse.return_value = [
            {"artist": "Artist1", "title": "Track1", "timestamp": "0:30"},
            {"artist": "Artist2", "title": "Track2", "timestamp": "3:45"}
        ]
        
        # Test function
        url = "https://www.1001tracklists.com/test"
        result = self.scraper.get_tracklist(url)
        
        # Assertions
        mock_fetch.assert_called_once_with(url)
        mock_parse.assert_called_once_with(self.sample_html)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["artist"], "Artist1")
        self.assertEqual(result[1]["title"], "Track2")


if __name__ == "__main__":
    unittest.main()