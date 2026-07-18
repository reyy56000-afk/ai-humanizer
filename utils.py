"""
Utility functions for AI Humanizer application.
Contains helper functions for text processing and validation.
"""
import re
from config import settings


def validate_text(text: str) -> tuple[bool, str]:
    """
    Validate input text for length and content.
    
    Args:
        text: The text to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not text or not isinstance(text, str):
        return False, "Text must be a non-empty string"
    
    text = text.strip()
    
    if len(text) < settings.min_text_length:
        return False, f"Text must be at least {settings.min_text_length} characters"
    
    if len(text) > settings.max_text_length:
        return False, f"Text must not exceed {settings.max_text_length} characters"
    
    return True, ""


def sanitize_text(text: str) -> str:
    """
    Sanitize text by removing extra whitespace and normalizing.
    
    Args:
        text: The text to sanitize
        
    Returns:
        Sanitized text
    """
    if not isinstance(text, str):
        return ""
    
    text = text.strip()
    # Remove extra whitespace (tabs, multiple spaces, etc.)
    text = re.sub(r'\s+', ' ', text)
    # Remove special Unicode spaces
    text = re.sub(r'[\u00A0\u1680\u2000-\u200A\u2028\u2029\u202F\u205F\u3000]', ' ', text)
    
    return text


def truncate_text(text: str, max_length: int) -> str:
    """
    Truncate text to maximum length.
    
    Args:
        text: The text to truncate
        max_length: Maximum length
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."


def count_words(text: str) -> int:
    """
    Count words in text accurately.
    
    Args:
        text: The text to count words in
        
    Returns:
        Number of words
    """
    if not isinstance(text, str) or not text.strip():
        return 0
    
    # Split on whitespace and filter empty strings
    words = [w for w in text.split() if w]
    return len(words)


def count_sentences(text: str) -> int:
    """
    Count sentences in text with improved accuracy for abbreviations.
    
    Args:
        text: The text to count sentences in
        
    Returns:
        Number of sentences
    """
    if not isinstance(text, str) or not text.strip():
        return 0
    
    # Common abbreviations that shouldn't end sentences
    abbreviations = r'\b(?:Dr|Mr|Mrs|Ms|Prof|Rev|Sr|Jr|Ph\.D|B\.A|M\.A|etc|vs|i\.e|e\.g)\.'
    
    # Replace sentence endings
    text = text.replace('...', '.')
    
    # Temporarily replace abbreviations with placeholder
    temp_text = re.sub(abbreviations, '<<<ABBR>>>', text, flags=re.IGNORECASE)
    
    # Split on sentence endings
    sentences = re.split(r'[.!?]+', temp_text)
    
    # Count non-empty sentences
    sentence_count = len([s for s in sentences if s.strip()])
    
    return max(1, sentence_count)  # At least 1 sentence


def get_text_complexity(text: str) -> dict:
    """
    Calculate text complexity metrics.
    
    Args:
        text: The text to analyze
        
    Returns:
        Dictionary with complexity metrics
    """
    if not isinstance(text, str) or not text.strip():
        return {"complexity": "unknown"}
    
    words = count_words(text)
    sentences = count_sentences(text)
    
    if sentences == 0:
        sentences = 1
    
    avg_words_per_sentence = words / sentences if sentences > 0 else 0
    
    # Simple complexity calculation
    if avg_words_per_sentence < 10:
        complexity = "simple"
    elif avg_words_per_sentence < 20:
        complexity = "moderate"
    else:
        complexity = "complex"
    
    return {
        "complexity": complexity,
        "words_per_sentence": round(avg_words_per_sentence, 2)
    }