from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
from dotenv import load_dotenv
import json
import asyncio
from groq import Groq
from services.nlp_processor import NLPProcessor

load_dotenv()

router = APIRouter()

# Initialize services
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
nlp_processor = NLPProcessor()

class BookSummaryRequest(BaseModel):
    title: str
    author: Optional[str] = None
    isbn: Optional[str] = None
    description: Optional[str] = None

class SummaryResponse(BaseModel):
    title: str
    author: Optional[str] = None
    overview: str
    chapter_breakdown: List[Dict[str, Any]]
    themes: List[str]
    characters: List[Dict[str, Any]]
    quotes: List[Dict[str, str]]
    key_terms: List[Dict[str, str]]
    discussion_questions: List[Dict[str, str]]
    visualizations: Dict[str, Any]

@router.post("/generate", response_model=SummaryResponse)
async def generate_book_summary(request: BookSummaryRequest):
    """
    Generate comprehensive book summary with analysis
    """
    try:
        # Prepare prompt for Groq
        prompt = f"""
        Generate a comprehensive analysis for the book "{request.title}" by {request.author or 'Unknown Author'}.
        
        Book Description: {request.description or 'No description provided'}
        
        Please provide:
        1. A detailed overview (2-3 paragraphs)
        2. Chapter-wise breakdown (5-8 chapters with summaries)
        3. Major themes (5-7 themes)
        4. Main characters (3-5 characters with descriptions)
        5. Important quotes (10 quotes with context)
        6. Key terms and definitions (8-12 terms)
        7. Discussion questions (10-15 questions with sample answers)
        8. Visualization data suggestions for:
           - Character relationship network
           - Timeline of events
           - Theme importance radar chart
           - Sentiment analysis arc
           - Geographic map of story locations
        
        Format the response as JSON with the following structure:
        {{
            "overview": "string",
            "chapter_breakdown": [{{"chapter": "string", "summary": "string"}}],
            "themes": ["string"],
            "characters": [{{"name": "string", "description": "string", "importance": "string"}}],
            "quotes": [{{"quote": "string", "context": "string", "chapter": "string"}}],
            "key_terms": [{{"term": "string", "definition": "string", "importance": "string"}}],
            "discussion_questions": [{{"question": "string", "sample_answer": "string"}}],
            "visualization_suggestions": {{
                "character_network": "description of nodes and edges",
                "timeline": "list of key events with approximate timing",
                "theme_radar": "list of themes for radar chart",
                "sentiment_arc": "description of emotional journey",
                "geographic_map": "list of important locations"
            }}
        }}
        
        Ensure the response is valid JSON only.
        """
        
        # Call Groq API
        chat_completion = groq_client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model="llama3-8b-8192",  # Using Llama 3 8B on Groq
            temperature=0.7,
            max_tokens=4000,
            top_p=1,
            stream=False
        )
        
        # Extract and parse the response
        response_text = chat_completion.choices[0].message.content
        
        # Try to extract JSON from the response
        try:
            # Find JSON-like content
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            if start_idx != -1 and end_idx != 0:
                json_str = response_text[start_idx:end_idx]
                summary_data = json.loads(json_str)
            else:
                # Fallback: create structured response from text
                summary_data = self._create_fallback_summary(response_text, request.title, request.author)
        except json.JSONDecodeError:
            # If JSON parsing fails, create a structured fallback
            summary_data = self._create_fallback_summary(response_text, request.title, request.author)
        
        # Enhance with NLP processing if we have a description
        if request.description:
            # Extract key terms using NLP
            key_terms_nlp = nlp_processor.extract_key_terms(request.description, num_terms=12)
            # Convert to expected format
            formatted_key_terms = []
            for term in key_terms_nlp:
                formatted_key_terms.append({
                    "term": term["term"],
                    "definition": term["definition"],
                    "importance": "High" if term["frequency"] > 2 else "Medium"
                })
            
            # Extract entities for characters
            entities = nlp_processor.extract_entities(request.description)
            characters_nlp = []
            for person in entities.get("PERSON", [])[:5]:  # Top 5 persons
                characters_nlp.append({
                    "name": person,
                    "description": f"Character mentioned in the book description",
                    "importance": "Medium"
                })
            
            # Extract quotes
            quotes_nlp = nlp_processor.extract_quotes(request.description, num_quotes=8)
            
            # Update summary data with NLP enhancements
            if formatted_key_terms:
                summary_data["key_terms"] = formatted_key_terms
            if characters_nlp:
                # Merge with existing characters or use NLP ones
                existing_chars = summary_data.get("characters", [])
                if not existing_chars:
                    summary_data["characters"] = characters_nlp
                else:
                    summary_data["characters"] = existing_chars + characters_nlp
            if quotes_nlp:
                summary_data["quotes"] = quotes_nlp
        
        # Generate chapter breakdown if not provided or weak
        if not summary_data.get("chapter_breakdown") or len(summary_data.get("chapter_breakdown", [])) < 3:
            # Use description or overview for chapter breakdown
            text_for_chapters = request.description or summary_data.get("overview", "")
            if text_for_chapters:
                summary_data["chapter_breakdown"] = nlp_processor.generate_chapter_breakdown(text_for_chapters, num_chapters=6)
        
        # Extract themes if not provided
        if not summary_data.get("themes"):
            # Simple theme extraction from key terms
            key_terms = summary_data.get("key_terms", [])
            themes = [term["term"] for term in key_terms[:5]] if key_terms else ["Literary Analysis", "Character Development", "Plot Structure"]
            summary_data["themes"] = list(set(themes))[:7]  # Deduplicate and limit
        
        # Generate discussion questions if not provided
        if not summary_data.get("discussion_questions"):
            summary_data["discussion_questions"] = self._generate_discussion_questions(summary_data)
        
        # Prepare final response
        response = SummaryResponse(
            title=request.title,
            author=request.author,
            overview=summary_data.get("overview", "Overview not available"),
            chapter_breakdown=summary_data.get("chapter_breakdown", []),
            themes=summary_data.get("themes", []),
            characters=summary_data.get("characters", []),
            quotes=summary_data.get("quotes", []),
            key_terms=summary_data.get("key_terms", []),
            discussion_questions=summary_data.get("discussion_questions", []),
            visualizations=summary_data.get("visualization_suggestions", {})
        )
        
        return response
        
    except Exce
