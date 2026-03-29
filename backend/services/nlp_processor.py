import spacy
import re
from typing import List, Dict, Any, Tuple
from collections import Counter
import logging

logger = logging.getLogger(__name__)

class NLPProcessor:
    def __init__(self):
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            logger.warning("spaCy model not found. Please run: python -m spacy download en_core_web_sm")
            # Create a blank English model as fallback
            self.nlp = spacy.blank("en")
            # Add sentencizer for sentence segmentation
            if "sentencizer" not in self.nlp.pipe_names:
                self.nlp.add_pipe("sentencizer")
    
    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """Extract named entities from text"""
        if not text or not self.nlp:
            return {"PERSON": [], "ORG": [], "GPE": [], "DATE": []}
        
        doc = self.nlp(text)
        entities = {
            "PERSON": [],
            "ORG": [],
            "GPE": [],  # Geopolitical entities
            "DATE": [],
            "WORK_OF_ART": []
        }
        
        for ent in doc.ents:
            if ent.label_ in entities:
                entities[ent.label_].append(ent.text)
        
        # Deduplicate and limit
        for key in entities:
            entities[key] = list(set(entities[key]))[:10]
        
        return entities
    
    def extract_key_terms(self, text: str, num_terms: int = 15) -> List[Dict[str, str]]:
        """Extract important terms and their definitions/context"""
        if not text or not self.nlp:
            return []
        
        doc = self.nlp(text)
        
        # Extract noun phrases and important words
        terms = []
        for chunk in doc.noun_chunks:
            # Filter out very short or common phrases
            if len(chunk.text.strip()) > 3 and chunk.text.lower() not in [
                'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'
            ]:
                terms.append({
                    "term": chunk.text.strip(),
                    "pos": "NOUN_PHRASE",
                    "frequency": 1
                })
        
        # Also extract important single words (adjectives, nouns)
        for token in doc:
            if (token.pos_ in ["NOUN", "ADJ"] and 
                not token.is_stop and 
                not token.is_punct and 
                len(token.text) > 2):
                terms.append({
                    "term": token.text,
                    "pos": token.pos_,
                    "frequency": 1
                })
        
        # Count frequencies
        term_counter = Counter()
        term_details = {}
        
        for term in terms:
            term_text = term["term"].lower()
            term_counter[term_text] += 1
            if term_text not in term_details:
                term_details[term_text] = term
        
        # Get top terms
        top_terms = term_counter.most_common(num_terms)
        
        result = []
        for term_text, freq in top_terms:
            if term_text in term_details:
                term_info = term_details[term_text].copy()
                term_info["frequency"] = freq
                # Generate a simple definition (in a real app, you'd use a dictionary API)
                term_info["definition"] = self._generate_definition(term_text, text)
                result.append(term_info)
        
        return result
    
    def _generate_definition(self, term: str, context: str) -> str:
        """Generate a simple definition based on context"""
        # This is a simplified version - in production you'd use WordNet or dictionary API
        sentences = re.split(r'[.!?]+', context)
        relevant_sentences = [s.strip() for s in sentences if term.lower() in s.lower()]
        
        if relevant_sentences:
            # Take the first relevant sentence and clean it up
            definition = relevant_sentences[0][:200] + ("..." if len(relevant_sentences[0]) > 200 else "")
            return definition
        else:
            return f"Important term related to the main themes of the text."
    
    def extract_quotes(self, text: str, num_quotes: int = 10) -> List[Dict[str, str]]:
        """Extract notable quotes from text"""
        if not text:
            return []
        
        # Simple quote extraction - look for quoted text
        quote_pattern = r'[""]([^""]{10,200})[""]'
        matches = re.findall(quote_pattern, text)
        
        quotes = []
        for match in matches[:num_quotes]:
            # Find context around the quote
            quote_pattern_full = rf'[""]{re.escape(match)}[""]'
            match_obj = re.search(quote_pattern_full, text)
            if match_obj:
                start = max(0, match_obj.start() - 100)
                end = min(len(text), match_obj.end() + 100)
                context = text[start:end].strip()
                
                quotes.append({
                    "quote": match.strip(),
                    "context": context,
                    "length": len(match.split())
                })
        
        # Sort by length (longer quotes might be more significant)
        quotes.sort(key=lambda x: x["length"], reverse=True)
        return [{"quote": q["quote"], "context": q["context"]} for q in quotes[:num_quotes]]
    
    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Basic sentiment analysis"""
        if not text or not self.nlp:
            return {"polarity": 0.0, "subjectivity": 0.0, "label": "NEUTRAL"}
        
        # Simple rule-based sentiment (in production, use TextBlob or transformers)
        positive_words = {"good", "great", "excellent", "amazing", "wonderful", "fantastic", 
                         "love", "liked", "enjoy", "happy", "joy", "best", "better", "positive"}
        negative_words = {"bad", "terrible", "awful", "horrible", "hate", "hated", "dislike",
                         "angry", "sad", "worst", "worse", "negative", "disappointing"}
        
        doc = self.nlp(text.lower())
        words = [token.text for token in doc if not token.is_stop and not token.is_punct]
        
        pos_count = sum(1 for word in words if word in positive_words)
        neg_count = sum(1 for word in words if word in negative_words)
        total = len(words)
        
        if total == 0:
            polarity = 0.0
        else:
            polarity = (pos_count - neg_count) / total
        
        # Subjectivity based on presence of opinion words
        opinion_words = positive_words.union(negative_words)
        opinion_count = sum(1 for word in words if word in opinion_words)
        subjectivity = opinion_count / total if total > 0 else 0.0
        
        label = "POSITIVE" if polarity > 0.1 else "NEGATIVE" if polarity < -0.1 else "NEUTRAL"
        
        return {
            "polarity": round(polarity, 3),
            "subjectivity": round(subjectivity, 3),
            "label": label
        }
    
    def extract_character_names(self, text: str) -> List[str]:
        """Extract potential character names from text"""
        if not text or not self.nlp:
            return []
        
        doc = self.nlp(text)
        person_ents = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
        
        # Also look for patterns like "Mr.", "Mrs.", "Dr." followed by names
        pattern = r'(?:Mr\.|Mrs\.|Ms\.|Dr\.|Prof\.)\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*'
        matches = re.findall(pattern, text)
        person_ents.extend(matches)
        
        # Clean and deduplicate
        cleaned = list(set([name.strip() for name in person_ents if len(name.strip()) > 2]))
        return sorted(cleaned)[:15]  # Return top 15
    
    def generate_chapter_breakdown(self, text: str, num_chapters: int = 8) -> List[Dict[str, str]]:
        """Generate a chapter-wise breakdown from text"""
        if not text:
            return [{"chapter": "Full Text", "summary": "Unable to generate chapter breakdown"}]
        
        # Split text into approximate chapters
        paragraphs = [p
