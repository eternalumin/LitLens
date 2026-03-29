import streamlit as st
import requests
import json
from datetime import datetime
import time
import os
from typing import Dict, Any, List

# Page configuration
st.set_page_config(
    page_title="LitLens - AI Book Analyzer",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #4b6cb7, #182848);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #4b6cb7;
        margin-bottom: 1rem;
    }
    .card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
    }
    .stButton > button {
        background: linear-gradient(90deg, #4b6cb7, #182848);
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-weight: bold;
        transition: all 0.3s;
    }
    .stButton > button:hover {
        background: linear-gradient(90deg, #3a5a94, #12203a);
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .quote-box {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0 5px 5px 0;
    }
    .term-box {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        padding: 0.75rem;
        margin: 0.5rem 0;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# API Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000/api/v1")

def init_session_state():
    """Initialize session state variables"""
    if 'book_data' not in st.session_state:
        st.session_state.book_data = None
    if 'summary_data' not in st.session_state:
        st.session_state.summary_data = None
    if 'loading' not in st.session_state:
        st.session_state.loading = False
    if 'history' not in st.session_state:
        st.session_state.history = []

def search_books(query: str) -> Dict[str, Any]:
    """Search for books using the backend API"""
    try:
        response = requests.get(f"{API_BASE_URL}/books/search", params={"q": query})
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error searching books: {response.status_code}")
            return {"books": []}
    except Exception as e:
        st.error(f"Connection error: {str(e)}")
        return {"books": []}

def get_book_details(book_id: str) -> Dict[str, Any]:
    """Get detailed book information"""
    try:
        response = requests.get(f"{API_BASE_URL}/books/{book_id}")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error fetching book details: {response.status_code}")
            return {}
    except Exception as e:
        st.error(f"Connection error: {str(e)}")
        return {}

def generate_summary(book_info: Dict[str, Any]) -> Dict[str, Any]:
    """Generate book summary using the backend API"""
    try:
        payload = {
            "title": book_info.get("title", ""),
            "author": book_info.get("author", ""),
            "isbn": book_info.get("isbn", ""),
            "description": book_info.get("description", "")
        }
        
        with st.spinner("🤖 AI is analyzing the book... This may take a moment."):
            response = requests.post(f"{API_BASE_URL}/summary/generate", json=payload)
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error generating summary: {response.status_code} - {response.text}")
            return {}
    except Exception as e:
        st.error(f"Connection error: {str(e)}")
        return {}

def display_summary(summary_data: Dict[str, Any]):
    """Display the generated book summary"""
    if not summary_data:
        st.warning("No summary data to display")
        return
    
    # Book header
    st.markdown(f'<h1 class="main-header">📚 LitLens Analysis</h1>', unsafe_allow_html=True)
    st.markdown(f'<p style="text-align: center; font-size: 1.2rem; color: #666;">{summary_data.get("title", "Unknown Book")}</p>', unsafe_allow_html=True)
    if summary_data.get('author'):
        st.markdown(f'<p style="text-align: center; font-size: 1rem; color: #888;">by {summary_data["author"]}</p>', unsafe_allow_html=True)
    
    st.divider()
    
    # Overview
    st.markdown('<h2 class="sub-header">📖 Overview</h2>', unsafe_allow_html=True)
    st.markdown(f'<div class="card">{summary_data.get("overview", "No overview available")}</div>', unsafe_allow_html=True)
    
    # Create tabs for different sections
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["🎯 Themes", "👥 Characters", "💬 Quotes", "📚 Terms", "❓ Discussion"])
    
    with tab1:
        if summary_data.get('themes'):
            st.markdown('<h3 class="sub-header">Key Themes</h3>', unsafe_allow_html=True)
            cols = st.columns(2)
            for i, theme in enumerate(summary_data['themes']):
                with cols[i % 2]:
                    st.markdown(f"""
                    <div class="term-box">
                        <strong>{theme}</strong>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("No themes identified")
    
    with tab2:
        if summary_data.get('characters'):
            st.markdown('<h3 class="sub-header">Main Characters</h3>', unsafe_allow_html=True)
            for char in summary_data['characters']:
                st.markdown(f"""
                <div class="card">
                    <h4>{char.get('name', 'Unknown Character')}</h4>
                    <p>{char.get('description', 'No description available')}</p>
                    {f"<p><em>Importance:</em> {char.get('importance', 'N/A')}</p>" if char.get('importance') else ""}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No character analysis available")
    
    with tab3:
        if summary_data.get('quotes'):
            st.markdown('<h3 class="sub-header">Important Quotes</h3>', unsafe_allow_html=True)
            for quote in summary_data['quotes'][:10]:  # Limit to 10 quotes
                st.markdown(f"""
                <div class="quote-box">
                    <em>"{quote.get('quote', '')}"</em><br>
                    <strong>— {quote.get('context', 'Context not available')}</strong>
                    {f"<br><small>Chapter: {quote.get('chapter', 'N/A')}</small>" if quote.get('chapter') else ""}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No quotes extracted")
    
    with tab4:
        if summary_data.get('key_terms'):
            st.markdown('<h3 class="sub-header">Key Terms & Definitions</h3>', unsafe_allow_html=True)
            for term in summary_data['key_terms']:
                st.markdown(f"""
                <div class="term-box">
                    <strong>{term.get('term', '')}</strong>: {term.get('definition', '')}
                    {f"<br><em>Importance:</em> {term.get('importance', 'N/A')}" if term.get('importance') else ""}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No key terms identified")
    
    with tab5:
        if summary_data.get('discussion_questions'):
            st.markdown('<h3 class="sub-header">Discussion Questions</h3>', unsafe_allow_html=True)
            for i, qa in enumerate(summary_data['discussion_questions'], 1):
                with st.expander(f"Question {i}: {qa.get('question', '')}"):
                   
