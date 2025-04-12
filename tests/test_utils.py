"""
Tests for the utils module.
"""
import unittest
from src.tracklist_chapter_fetch.utils import validate_url, format_time_ms, ValidationError


class TestUtils(unittest.TestCase):
    def test_validate_url_valid(self):
        """Test URL validation with valid 1001tracklists URLs."""
        valid_urls = [
            "https://www.1001tracklists.com/tracklist/12345",
            "http://1001tracklists.com/tracklist/abcdef",
            "https://1001tracklists.com/tracklist/295f7nbt/steve-angello-an21-size-sound-system-055-2025-03-20.html"
        ]
        
        for url in valid_urls:
            try:
                result = validate_url(url)
                self.assertTrue(result, f"URL validation should succeed for {url}")
            except ValidationError:
                self.fail(f"validate_url raised ValidationError unexpectedly for {url}")

    def test_validate_url_invalid(self):
        """Test URL validation with invalid URLs."""
        invalid_urls = [
            "",
            "not-a-url",
            "http://example.com",
            "https://www.otherdomain.com/tracklist/12345"
        ]
        
        for url in invalid_urls:
            with self.assertRaises(ValidationError):
                validate_url(url)

    def test_format_time_ms(self):
        """Test timestamp conversion to milliseconds."""
        test_cases = [
            ("0:34", 34 * 1000),
            ("1:15", 75 * 1000),
            ("01:30", 90 * 1000),
            ("1:00:00", 3600 * 1000),
            ("1:30:45", (1 * 3600 + 30 * 60 + 45) * 1000),
            ("invalid", None),
            ("", None),
        ]
        
        for time_str, expected in test_cases:
            result = format_time_ms(time_str)
            self.assertEqual(result, expected, f"format_time_ms({time_str}) should return {expected}")


if __name__ == "__main__":
    unittest.main()