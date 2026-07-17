"""
AI Detection module for identifying AI-generated text.
Uses machine learning patterns and heuristics to detect AI content.
"""
from ollama import chat
from prompts import DETECTOR_PROMPT
from config import settings
import re


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
        response = chat(
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
        return {
            "is_ai": None,
            "analysis": str(e),
            "confidence": 0,
            "success": False,
            "error": str(e)
        }


def parse_ai_detection(response: str) -> bool:
    """
    Parse AI detection response.
    
    Args:
        response: Response from LLM
        
    Returns:
        Boolean indicating if likely AI-generated
    """
    response_lower = response.lower()
    
    if "ai-generated" in response_lower or "likely ai" in response_lower:
        return True
    elif "human" in response_lower:
        return False
    
    return False


def extract_confidence(response: str) -> int:
    """
    Extract confidence percentage from response.
    
    Args:
        response: Response from LLM
        
    Returns:
        Confidence percentage (0-100)
    """
    numbers = re.findall(r'\b(\d{1,3})\s*%', response)
    
    if numbers:
        confidence = int(numbers[0])
        return min(100, max(0, confidence))
    
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
    
    # Check for passive voice
    if re.search(r'\bwas\s+\w+ed\b', text):
        indicators.append("Excessive passive voice usage")
    
    # Check for formal patterns
    if re.search(r'\b(furthermore|moreover|in conclusion|it is|there are)\b', text.lower()):
        indicators.append("Formal transition patterns")
    
    # Check for long sentences
    sentences = text.split('.')
    long_sentences = [s for s in sentences if len(s.split()) > 25]
    if len(long_sentences) / max(len(sentences), 1) > 0.3:
        indicators.append("High proportion of long sentences")
    
    return indicators
