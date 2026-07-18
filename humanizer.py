"""
Enhanced Humanizer module for converting AI text to human-like writing.
Handles various text processing and enhancement tasks.
"""
import logging
import ollama
from prompts import HUMANIZE_PROMPT, IMPROVE_PROMPT, SUMMARIZE_PROMPT, TONE_ADJUST_PROMPT
from config import settings
from utils import validate_text, sanitize_text

logger = logging.getLogger(__name__)


def humanize_text(text: str) -> dict:
    """
    Convert AI-generated text to sound naturally human-written.
    
    Args:
        text: Text to humanize
        
    Returns:
        Dictionary with humanized text and metadata
    """
    # Sanitize text FIRST, then validate
    text = sanitize_text(text)
    
    # Validate input
    is_valid, error_msg = validate_text(text)
    if not is_valid:
        return {
            "success": False,
            "error": error_msg,
            "humanized": None
        }
    
    prompt = HUMANIZE_PROMPT.format(text=text)
    
    try:
        client = ollama.Client(base_url=settings.ollama_host)
        response = client.chat(
            model=settings.ollama_model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            stream=False,
        )
        
        humanized_text = response["message"]["content"].strip()
        
        return {
            "success": True,
            "original": text,
            "humanized": humanized_text,
            "model": settings.ollama_model,
            "char_count": len(humanized_text),
            "word_count": len(humanized_text.split())
        }
    except Exception as e:
        logger.error(f"Error humanizing text: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "humanized": None
        }


def improve_text(text: str) -> dict:
    """
    Improve text for clarity and professionalism.
    
    Args:
        text: Text to improve
        
    Returns:
        Dictionary with improved text and metadata
    """
    # Sanitize first, then validate
    text = sanitize_text(text)
    
    is_valid, error_msg = validate_text(text)
    if not is_valid:
        return {
            "success": False,
            "error": error_msg,
            "improved": None
        }
    
    prompt = IMPROVE_PROMPT.format(text=text)
    
    try:
        client = ollama.Client(base_url=settings.ollama_host)
        response = client.chat(
            model=settings.ollama_model,
            messages=[{"role": "user", "content": prompt}],
            stream=False,
        )
        
        improved_text = response["message"]["content"].strip()
        
        return {
            "success": True,
            "original": text,
            "improved": improved_text,
            "model": settings.ollama_model
        }
    except Exception as e:
        logger.error(f"Error improving text: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "improved": None
        }


def summarize_text(text: str) -> dict:
    """
    Summarize text concisely.
    
    Args:
        text: Text to summarize
        
    Returns:
        Dictionary with summary and metadata
    """
    # Sanitize first, then validate
    text = sanitize_text(text)
    
    is_valid, error_msg = validate_text(text)
    if not is_valid:
        return {
            "success": False,
            "error": error_msg,
            "summary": None
        }
    
    prompt = SUMMARIZE_PROMPT.format(text=text)
    
    try:
        client = ollama.Client(base_url=settings.ollama_host)
        response = client.chat(
            model=settings.ollama_model,
            messages=[{"role": "user", "content": prompt}],
            stream=False,
        )
        
        summary_text = response["message"]["content"].strip()
        
        return {
            "success": True,
            "original": text,
            "original_length": len(text),
            "summary": summary_text,
            "summary_length": len(summary_text),
            "compression_ratio": len(summary_text) / len(text) if len(text) > 0 else 0,
            "model": settings.ollama_model
        }
    except Exception as e:
        logger.error(f"Error summarizing text: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "summary": None
        }


def adjust_tone(text: str, tone: str) -> dict:
    """
    Adjust text tone (professional, casual, formal, friendly, persuasive, technical).
    
    Args:
        text: Text to adjust
        tone: Desired tone
        
    Returns:
        Dictionary with adjusted text
    """
    valid_tones = ["professional", "casual", "formal", "friendly", "persuasive", "technical"]
    
    if tone.lower() not in valid_tones:
        return {
            "success": False,
            "error": f"Invalid tone. Choose from: {', '.join(valid_tones)}",
            "adjusted": None
        }
    
    # Sanitize first, then validate
    text = sanitize_text(text)
    
    is_valid, error_msg = validate_text(text)
    if not is_valid:
        return {
            "success": False,
            "error": error_msg,
            "adjusted": None
        }
    
    prompt = TONE_ADJUST_PROMPT.format(text=text, tone=tone)
    
    try:
        client = ollama.Client(base_url=settings.ollama_host)
        response = client.chat(
            model=settings.ollama_model,
            messages=[{"role": "user", "content": prompt}],
            stream=False,
        )
        
        adjusted_text = response["message"]["content"].strip()
        
        return {
            "success": True,
            "original": text,
            "adjusted": adjusted_text,
            "tone": tone,
            "model": settings.ollama_model
        }
    except Exception as e:
        logger.error(f"Error adjusting tone: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "adjusted": None
        }


def batch_humanize(texts: list) -> list:
    """
    Humanize multiple texts in batch.
    
    Args:
        texts: List of texts to humanize
        
    Returns:
        List of humanized results
    """
    results = []
    for text in texts:
        result = humanize_text(text)
        results.append(result)
    
    return results