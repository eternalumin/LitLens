from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
import requests
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

OPEN_LIBRARY_API = "https://openlibrary.org"
GOOGLE_BOOKS_API = "https://www.googleapis.com/books/v1/volumes"

@router.get("/search")
async def search_books(q: str = Query(..., description="Book title or author")):
    """
    Search for books using Open Library API
    """
    try:
        # Open Library search
        response = requests.get(f"{OPEN_LIBRARY_API}/search.json", params={"q": q, "limit": 10})
        response.raise_for_status()
        data = response.json()
        
        books = []
        for doc in data.get("docs", [])[:5]:  # Limit to 5 results
            book_info = {
                "title": doc.get("title"),
                "author": doc.get("author_name", [])[0] if doc.get("author_name") else "Unknown",
                "publish_year": doc.get("first_publish_year"),
                "isbn": doc.get("isbn", [])[0] if doc.get("isbn") else None,
                "cover_id": doc.get("cover_i"),
                "openlibrary_key": doc.get("key")
            }
            books.append(book_info)
        
        return {"books": books, "query": q}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching books: {str(e)}")

@router.get("/{book_id}")
async def get_book_details(book_id: str):
    """
    Get detailed information about a book by Open Library ID
    """
    try:
        # Get book details from Open Library
        response = requests.get(f"https://openlibrary.org{book_id}.json")
        response.raise_for_status()
        book_data = response.json()
        
        # Get author info if available
        authors = []
        if "authors" in book_data:
            for author in book_data["authors"]:
                if "author" in author and "key" in author["author"]:
                    author_response = requests.get(f"https://openlibrary.org{author['author']['key']}.json")
                    if author_response.status_code == 200:
                        author_data = author_response.json()
                        authors.append({
                            "name": author_data.get("name"),
                            "bio": author_data.get("bio", {}).get("value") if isinstance(author_data.get("bio"), dict) else author_data.get("bio")
                        })
        
        details = {
            "title": book_data.get("title"),
            "authors": authors,
            "publish_date": book_data.get("publish_date"),
            "publishers": book_data.get("publishers", []),
            "number_of_pages": book_data.get("number_of_pages"),
            "isbn_10": book_data.get("isbn_10"),
            "isbn_13": book_data.get("isbn_13"),
            "description": book_data.get("description", {}).get("value") if isinstance(book_data.get("description"), dict) else book_data.get("description"),
            "subjects": book_data.get("subjects", [])[:10],  # Limit subjects
            "cover_url": f"https://covers.openlibrary.org/b/id/{book_data.get('cover_id')}-L.jpg" if book_data.get('cover_id') else None
        }
        
        return details
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching book details: {str(e)}")
