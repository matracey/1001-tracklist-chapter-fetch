"""
Web scraping functionality for extracting tracklists from 1001tracklists.com.
"""

import time
from typing import Any, Dict, List

import requests
from fake_useragent import UserAgent
from scrapling.parser import Adaptor

from .utils import logger


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
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": self.ua.chrome})

    def fetch_page(self, url: str) -> Adaptor:
        """
        Fetch HTML content from the specified URL.

        Args:
            url: URL to fetch content from

        Returns:
            Adaptor object containing the HTML content

        Raises:
            ScrapingError: If the request fails or returns non-200 status code
        """
        logger.debug("Fetching URL: %s", url)
        try:
            # Add delay to avoid hitting rate limits
            time.sleep(1)

            response = self.session.get(url, timeout=30)

            if response.status_code != 200:
                raise ScrapingError(
                    f"Failed to fetch page. Status code: {response.status_code}"
                )

            logger.debug("Successfully fetched page content")
            return Adaptor(response.text)
        except requests.RequestException as e:
            raise ScrapingError(f"Error fetching page: {str(e)}") from e

    def __extract_title__(self, item: Any, selectors: List[str]) -> str:
        """
        Extract the title from a track item.

        Args:
            item: Track item element
            selectors: List of CSS selectors to try

        Returns:
            The extracted title
        """
        for selector in selectors:
            title_elem = item.css(selector)
            if title_elem:
                return title_elem[0].text.strip()

        logger.warning("Could not find track title, using default")
        return "Unknown Track"

    def get_tracklist(self, url: str) -> List[Dict[str, Any]]:
        """
        Fetch and parse tracklist data from a 1001tracklists URL.

        Args:
            url: 1001tracklists URL to fetch and parse

        Returns:
            List of track dictionaries

        Raises:
            ScrapingError: If fetching or parsing fails
        """
        try:
            page_adaptor = self.fetch_page(url)
            return {}
        except Exception as e:
            raise ScrapingError(f"Failed to parse tracklist: {str(e)}") from e
