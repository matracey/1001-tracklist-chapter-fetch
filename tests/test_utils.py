"""
Tests for the utils module.
"""

import unittest

from src.tracklist_chapter_fetch.utils import ValidationError, validate_url


class TestUtils(unittest.TestCase):
    def test_validate_url_valid(self):
        """Test URL validation with valid 1001tracklists URLs."""
        valid_urls = [
            "https://www.1001tracklists.com/tracklist/12345",
            "http://1001tracklists.com/tracklist/abcdef",
            "https://1001tracklists.com/tracklist/295f7nbt/steve-angello-an21-size-sound-system-055-2025-03-20.html",
        ]

        for url in valid_urls:
            try:
                result = validate_url(url)
                self.assertTrue(result, f"URL validation should succeed for {url}")
            except ValidationError:
                self.fail(f"validate_url raised ValidationError unexpectedly for {url}")


if __name__ == "__main__":
    unittest.main()
