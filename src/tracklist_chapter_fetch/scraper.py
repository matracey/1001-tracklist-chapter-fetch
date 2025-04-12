"""
Web scraping functionality for extracting tracklists from 1001tracklists.com.
"""
import time
import logging
from typing import List, Dict, Optional, Any
import re

from bs4 import BeautifulSoup
import requests

from .utils import logger

class ScrapingError(Exception):
    """Exception raised for scraping errors."""
    pass

class TracklistScraper:
    """
    Scraper for 1001tracklists.com to extract tracklist information.
    """
    
    def __init__(self, user_agent: str = None):
        """
        Initialize the scraper with optional user agent.
        
        Args:
            user_agent: Optional user agent string for HTTP requests
        """
        self.user_agent = user_agent or "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': self.user_agent})
    
    def fetch_page(self, url: str) -> str:
        """
        Fetch HTML content from the specified URL.
        
        Args:
            url: URL to fetch content from
            
        Returns:
            HTML content as string
            
        Raises:
            ScrapingError: If the request fails or returns non-200 status code
        """
        logger.debug(f"Fetching URL: {url}")
        try:
            # Add delay to avoid hitting rate limits
            time.sleep(1)
            
            response = self.session.get(url, timeout=30)
            
            if response.status_code != 200:
                raise ScrapingError(f"Failed to fetch page. Status code: {response.status_code}")
                
            logger.debug("Successfully fetched page content")
            return response.text
        except requests.RequestException as e:
            raise ScrapingError(f"Error fetching page: {str(e)}")
    
    def parse_tracklist(self, html_content: str) -> List[Dict[str, Any]]:
        """
        Extract tracks from 1001tracklists HTML content.
        
        Args:
            html_content: Raw HTML content from the tracklist page
            
        Returns:
            List of track dictionaries with 'artist', 'title', and 'timestamp' fields
            
        Raises:
            ScrapingError: If parsing fails
        """
        logger.debug("Parsing tracklist content...")
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Extract the main tracklist container - try different potential selectors
        try:
            # Try different possible container selectors
            container_selectors = [
                "div.tlpContainer",
                "div#tlp_container",
                "div.tlpItemsContainer",
                "div#tlplist",
                "div.tl-container"
            ]
            
            tracklist_container = None
            for selector in container_selectors:
                container = soup.select_one(selector)
                if container:
                    tracklist_container = container
                    logger.debug(f"Found tracklist container using selector: {selector}")
                    break
            
            if not tracklist_container:
                # Try to find any div that might contain track items
                logger.debug("Attempting to find track items directly...")
                track_selectors = [
                    "div.tlpItem",
                    "div.tl-item",
                    "div.tracklistItem",
                    "div[data-track]"
                ]
                
                for selector in track_selectors:
                    track_items = soup.select(selector)
                    if track_items:
                        logger.debug(f"Found track items directly with selector: {selector}")
                        # If we found track items directly, create a container for them
                        tracklist_container = soup.new_tag("div")
                        for item in track_items:
                            tracklist_container.append(item)
                        break
            
            if not tracklist_container:
                # Last resort: log part of the HTML for debugging
                logger.debug("HTML structure sample:")
                body = soup.find('body')
                if body:
                    logger.debug(body.prettify()[:500] + "...")
                raise ScrapingError("Could not find tracklist container in the page")
                
            # Extract the tracklist title for debugging
            tracklist_title = soup.select_one("meta[property='og:title']") or soup.select_one("title")
            if tracklist_title:
                title_content = tracklist_title.get("content", tracklist_title.text if hasattr(tracklist_title, "text") else "Unknown Tracklist")
                logger.debug(f"Processing tracklist: {title_content}")
                
            # Find all track items - try different track item selectors
            track_item_selectors = [
                "div.tlpItem",
                "div.tl-item", 
                "div.tracklistItem", 
                "div[data-track]"
            ]
            
            track_items = []
            for selector in track_item_selectors:
                items = tracklist_container.select(selector)
                if items:
                    logger.debug(f"Found {len(items)} track items using selector: {selector}")
                    track_items = items
                    break
            
            if not track_items:
                raise ScrapingError("No track items found in the tracklist")
                
            logger.info(f"Found {len(track_items)} tracks in the tracklist")
            
            # Try different selectors for timestamps, artists, and titles
            timestamp_selectors = [
                "div.tlpCuePointTimecode span.tcWrap",
                "div.cue-time", 
                "span.time", 
                "span.timestamp",
                "div.tl-time"
            ]
            
            artist_selectors = [
                "span.blueTxt a",
                "div.tl-artist", 
                "span.artist a", 
                "div.artist-name"
            ]
            
            title_selectors = [
                "span.trackValue",
                "div.tl-title", 
                "span.title", 
                "div.track-title"
            ]
            
            tracks = []
            for item in track_items:
                try:
                    # Extract timestamp using multiple potential selectors
                    timestamp = None
                    for selector in timestamp_selectors:
                        timestamp_elem = item.select_one(selector)
                        if timestamp_elem:
                            timestamp = timestamp_elem.text.strip()
                            logger.debug(f"Found timestamp '{timestamp}' using selector: {selector}")
                            break
                    
                    # If we still don't have a timestamp, look for any element with time-like content
                    if not timestamp:
                        for elem in item.find_all(text=re.compile(r'\d+:\d+')):
                            timestamp = elem.strip()
                            logger.debug(f"Found timestamp using regex: {timestamp}")
                            break
                    
                    # Get the track title - this often includes both artist and title info
                    track_full_title = None
                    for selector in title_selectors:
                        title_elem = item.select_one(selector)
                        if title_elem:
                            track_full_title = title_elem.text.strip()
                            logger.debug(f"Found track text: '{track_full_title}'")
                            break
                    
                    if not track_full_title:
                        track_full_title = "Unknown Track"
                        logger.warning("Could not find track title, using default")
                    
                    # Check if the track title already contains artist information (common format: "Artist - Title")
                    track_info = {"title": track_full_title, "artist": None, "timestamp": timestamp}
                    
                    # For output that matches the example format in the requirements,
                    # we'll use the full track text as is since it usually contains 
                    # the format "Artist - Title" already
                    
                    # Add to tracks list if timestamp exists
                    if timestamp:
                        tracks.append(track_info)
                        logger.debug(f"Added track: {track_full_title} ({timestamp})")
                    else:
                        logger.warning(f"Skipping track without timestamp: {track_full_title}")
                        
                except Exception as e:
                    logger.warning(f"Error parsing track item: {str(e)}")
            
            if not tracks:
                raise ScrapingError("Failed to extract any valid track information")
                
            return tracks
            
        except Exception as e:
            raise ScrapingError(f"Failed to parse tracklist: {str(e)}")
    
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
        html_content = self.fetch_page(url)
        return self.parse_tracklist(html_content)