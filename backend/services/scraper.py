import requests
import json
from typing import Dict, List, Optional
from bs4 import BeautifulSoup
import time
import random
from urllib.parse import quote_plus
import logging

logger = logging.getLogger(__name__)

class BookScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def search_open_library(self, query: str, limit: int = 10) -> List[Dict]:
        """Search Open Library for books"""
        try:
            url = "https://openlibrary.org/search.json"
            params = {
                'q': query,
                'limit': limit
            }
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            books = []
            for doc in data.get('docs', []):
                book = {
                    'title': doc.get('title'),
                    'author': doc.get('author_name', [])[0] if doc.get('author_name') else 'Unknown',
                    'publish_year': doc.get('first_publish_year'),
                    'isbn': doc.get('isbn', [])[0] if doc.get('isbn') else None,
                    'cover_id': doc.get('cover_i'),
                    'olid': doc.get('olid'),
                    'key': doc.get('key')
                }
                books.append(book)
            
            return books
        except Exception as e:
            logger.error(f"Error searching Open Library: {e}")
            return []
    
    def get_book_details(self, olid: str) -> Optional[Dict]:
        """Get detailed book information from Open Library"""
        try:
            url = f"https://openlibrary.org/olids/{olid}.json"
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error fetching book details: {e}")
            return None
    
    def get_book_description(self, olid: str) -> Optional[str]:
        """Get book description from Open Library"""
        try:
            book_data = self.get_book_details(olid)
            if book_data and 'description' in book_data:
                desc = book_data['description']
                if isinstance(desc, dict) and 'value' in desc:
                    return desc['value']
                elif isinstance(desc, str):
                    return desc
            return None
        except Exception as e:
            logger.error(f"Error fetching book description: {e}")
            return None
    
    def scrape_wikipedia_summary(self, title: str, author: str = "") -> Optional[str]:
        """Scrape Wikipedia for book summary"""
        try:
            search_query = f"{title} {author} book".strip()
            url = f"https://en.wikipedia.org/w/index.php?search={quote_plus(search_query)}&title=Special:Search&fulltext=1"
            
            response = self.session.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for the first few paragraphs after the infobox
            content_div = soup.find('div', {'id': 'mw-content-text'})
            if not content_div:
                return None
            
            paragraphs = content_div.find_all('p')
            summary_parts = []
            
            for p in paragraphs[:3]:  # Get first 3 paragraphs
                text = p.get_text().strip()
                if text and not text.startswith('[') and len(text) > 50:
                    summary_parts.append(text)
            
            return ' '.join(summary_parts) if summary_parts else None
            
        except Exception as e:
            logger.error(f"Error scraping Wikipedia: {e}")
            return None
    
    def get_google_books_info(self, isbn: str) -> Optional[Dict]:
        """Get book information from Google Books API"""
        try:
            if not isbn:
                return None
                
            url = f"https://www.googleapis.com/books/v1/volumes"
            params = {'q': f'isbn:{isbn}'}
            
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data.get('totalItems', 0) > 0:
                volume_info = data['items'][0]['volumeInfo']
                return {
                    'title': volume_info.get('title'),
                    'authors': volume_info.get('authors', []),
                    'published_date': volume_info.get('publishedDate'),
                    'description': volume_info.get('description'),
                    'page_count': volume_info.get('pageCount'),
                    'categories': volume_info.get('categories', []),
                    'average_rating': volume_info.get('averageRating'),
                    'thumbnail': volume_info.get('imageLinks', {}).get('thumbnail')
                }
            return None
        except Exception as e:
            logger.error(f"Error fetching Google Books info: {e}")
            return None

# Global scraper instance
scraper = BookScraper()
