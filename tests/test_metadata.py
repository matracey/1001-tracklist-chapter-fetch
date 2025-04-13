"""
Tests for the metadata module.
"""

import unittest

from src.tracklist_chapter_fetch.metadata import MetadataError, generate_ffmetadata


class TestMetadata(unittest.TestCase):
    def test_generate_ffmetadata(self):
        """Test generating FFMETADATA from track info."""
        tracks = [
            {"artist": "Artist1", "title": "Title1", "timestamp": "0:34"},
            {"artist": "Artist2", "title": "Title2", "timestamp": "3:53"},
            {"artist": "Artist3", "title": "Title3", "timestamp": "7:42"},
        ]

        metadata = generate_ffmetadata(tracks)

        # Check the header
        self.assertTrue(
            metadata.startswith(";FFMETADATA1"),
            "Metadata should start with ;FFMETADATA1",
        )

        # Check that each track is included
        self.assertIn("Artist1 - Title1", metadata)
        self.assertIn("Artist2 - Title2", metadata)
        self.assertIn("Artist3 - Title3", metadata)

        # Check timestamp conversions (0:34 = 34000ms)
        self.assertIn("START=34000", metadata)
        self.assertIn("START=233000", metadata)  # 3:53 = 233000ms
        self.assertIn("START=462000", metadata)  # 7:42 = 462000ms

    def test_generate_ffmetadata_empty(self):
        """Test error handling with empty track list."""
        with self.assertRaises(MetadataError):
            generate_ffmetadata([])


if __name__ == "__main__":
    unittest.main()
