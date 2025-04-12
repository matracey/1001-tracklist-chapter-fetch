"""
Tests for the metadata module.
"""
import unittest
import os
import tempfile
from src.tracklist_chapter_fetch.metadata import generate_ffmetadata, save_metadata_to_file, MetadataError


class TestMetadata(unittest.TestCase):
    def test_generate_ffmetadata(self):
        """Test generating FFMETADATA from track info."""
        tracks = [
            {"artist": "Artist1", "title": "Title1", "timestamp": "0:34"},
            {"artist": "Artist2", "title": "Title2", "timestamp": "3:53"},
            {"artist": "Artist3", "title": "Title3", "timestamp": "7:42"}
        ]
        
        metadata = generate_ffmetadata(tracks)
        
        # Check the header
        self.assertTrue(metadata.startswith(";FFMETADATA1"), "Metadata should start with ;FFMETADATA1")
        
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
    
    def test_save_metadata_to_file(self):
        """Test saving metadata to a file."""
        test_metadata = ";FFMETADATA1\n[CHAPTER]\nTIMEBASE=1/1000\nSTART=0\nEND=1000\ntitle=Test"
        
        # Create a temporary file for testing
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            temp_path = tmp.name
        
        try:
            save_metadata_to_file(test_metadata, temp_path)
            
            # Check that the file exists and has the correct content
            self.assertTrue(os.path.exists(temp_path))
            
            with open(temp_path, 'r', encoding='utf-8') as f:
                content = f.read()
                self.assertEqual(content, test_metadata)
                
        finally:
            # Clean up the temporary file
            if os.path.exists(temp_path):
                os.unlink(temp_path)


if __name__ == "__main__":
    unittest.main()