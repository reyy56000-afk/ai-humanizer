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
    Sanitize text by removing extra whitespace.
    
    Args:
        text: The text to sanitize
        
    Returns:
        Sanitized text
    """
    text = text.strip()
    text = re.sub(r'\s+', ' ', text)
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
    Count words in text.
    
    Args:
        text: The text to count words in
        
    Returns:
        Number of words
    """
    return len(text.split())


def count_sentences(text: str) -> int:
    """
    Count sentences in text.
    
    Args:
        text: The text to count sentences in
        
    Returns:
        Number of sentences
    """
    sentences = re.split(r'[.!?]+', text)
    return len([s for s in sentences if s.strip()])
