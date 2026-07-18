"""
AI Detection module for identifying AI-generated text.
Uses machine learning patterns and heuristics to detect AI content.
"""
import logging
import re
import ollama
from prompts import DETECTOR_PROMPT
from config import settings

logger = logging.getLogger(__name__)


def detect_ai_text(text: str) -> dict:
    """
    Detect if text is likely AI-generated using Ollama.
    
    Args:
        text: Text to analyze
        
    Returns:
        Dictionary with detection results
    """
    prompt = DETECTOR_PROMPT.format(text=text)
    
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
        
        result_text = response["message"]["content"]
        
        return {
            "is_ai": parse_ai_detection(result_text),
            "analysis": result_text,
            "confidence": extract_confidence(result_text),
            "success": True
        }
    except Exception as e:
        logger.error(f"Error detecting AI text: {str(e)}")
        return {
            "is_ai": None,
            "analysis": str(e),
            "confidence": 0,
            "success": False,
            "error": str(e)
        }


def parse_ai_detection(response: str) -> bool:
    """
    Parse AI detection response with improved logic.
    
    Args:
        response: Response from LLM
        
    Returns:
        Boolean indicating if likely AI-generated
    """
    response_lower = response.lower()
    
    # More robust detection patterns
    ai_indicators = [
        "ai-generated",
        "likely ai",
        "ai generated",
        "appears to be generated",
        "machine-generated",
        "artificial intelligence",
        "verdict: ai",
        "verdict:ai",
    ]
    
    human_indicators = [
        "human-written",
        "human written",
        "verdict: human",
        "verdict:human",
        "appears human",
        "genuinely human",
    ]
    
    # Check for AI indicators
    for indicator in ai_indicators:
        if indicator in response_lower:
            return True
    
    # Check for human indicators (overrides ambiguous cases)
    for indicator in human_indicators:
        if indicator in response_lower:
            return False
    
    # Fallback: check confidence percentage
    confidence = extract_confidence(response)
    if confidence >= 50:
        return True
    
    return False


def extract_confidence(response: str) -> int:
    """
    Extract confidence percentage from response.
    
    Args:
        response: Response from LLM
        
    Returns:
        Confidence percentage (0-100)
    """
    # Look for percentage patterns like "85%" or "85 %"
    numbers = re.findall(r'\b(\d{1,3})\s*%', response)
    
    if numbers:
        try:
            confidence = int(numbers[0])
            return min(100, max(0, confidence))
        except (ValueError, IndexError):
            return 0
    
    return 0


def get_ai_indicators(text: str) -> list:
    """
    Extract AI writing indicators from text.
    
    Args:
        text: Text to analyze
        
    Returns:
        List of detected indicators
    """
    indicators = []
    
    # Check for repeated phrases
    words = text.lower().split()
    word_freq = {}
    for word in words:
        word_freq[word] = word_freq.get(word, 0) + 1
    
    repeated = [word for word, count in word_freq.items() if count > 5 and len(word) > 4]
    if repeated:
        indicators.append(f"Repeated words/phrases: {', '.join(repeated[:3])}")
    
    # Check for passive voice (improved pattern)
    passive_pattern = r'\b(was|were|is|are|be)\s+\w+(?:ed|en)\b'
    passive_matches = len(re.findall(passive_pattern, text))
    total_words = len(words)
    
    if total_words > 0 and (passive_matches / total_words) > 0.15:
        indicators.append(f"Excessive passive voice usage ({passive_matches} instances)")
    
    # Check for formal patterns
    formal_patterns = [
        r'\b(furthermore|moreover|in conclusion|it is|there are|in addition)\b',
        r'\b(undoubtedly|arguably|consequently|accordingly)\b'
    ]
    
    formal_count = sum(len(re.findall(pattern, text.lower())) for pattern in formal_patterns)
    if formal_count >= 3:
        indicators.append(f"Formal transition patterns ({formal_count} found)")
    
    # Check for long sentences (improved)
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    if len(sentences) > 0:
        long_sentences = [s for s in sentences if len(s.split()) > 25]
        long_ratio = len(long_sentences) / len(sentences)
        
        if long_ratio > 0.3:
            indicators.append(f"High proportion of long sentences ({long_ratio:.0%})")
    
    return indicators if indicators else ["No obvious AI indicators detected"]