"""
Web scraping functionality for extracting tracklists from 1001tracklists.com.
"""

from fake_useragent import UserAgent


class ScrapingError(Exception):
    """Exception raised for scraping errors."""


class TracklistScraper:
    """
    Scraper for 1001tracklists.com to extract tracklist information.
    """

    def __init__(self):
        """
        Initialize the scraper.
        """
        self.ua: UserAgent = UserAgent()
