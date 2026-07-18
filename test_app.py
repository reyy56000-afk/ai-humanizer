"""
Test suite for AI Humanizer application.
Contains unit tests for all major functions.
"""
import pytest
from fastapi.testclient import TestClient
from app import app
from humanizer import humanize_text, improve_text, summarize_text, adjust_tone
from detector import detect_ai_text, parse_ai_detection, extract_confidence
from utils import validate_text, count_words, count_sentences, sanitize_text, get_text_complexity


client = TestClient(app)


# ==================== Utility Tests ====================

class TestUtilities:
    """Test utility functions."""
    
    def test_validate_text_valid(self):
        """Test validation with valid text."""
        is_valid, error = validate_text("This is a valid test text.")
        assert is_valid is True
        assert error == ""
    
    def test_validate_text_empty(self):
        """Test validation with empty text."""
        is_valid, error = validate_text("")
        assert is_valid is False
        assert "non-empty" in error
    
    def test_validate_text_too_short(self):
        """Test validation with too short text."""
        is_valid, error = validate_text("short")
        assert is_valid is False
        assert "at least" in error
    
    def test_sanitize_text(self):
        """Test text sanitization."""
        text = "This   has    extra    spaces"
        result = sanitize_text(text)
        assert "   " not in result
        assert result == "This has extra spaces"
    
    def test_count_words(self):
        """Test word counting."""
        text = "This is a test text"
        assert count_words(text) == 5
    
    def test_count_words_empty(self):
        """Test word counting with empty string."""
        assert count_words("") == 0
        assert count_words("   ") == 0
    
    def test_count_sentences(self):
        """Test sentence counting."""
        text = "This is a test. This is another. And one more!"
        assert count_sentences(text) == 3
    
    def test_count_sentences_with_abbreviations(self):
        """Test sentence counting with abbreviations."""
        text = "Dr. Smith went to the store. He bought milk."
        count = count_sentences(text)
        assert count == 2
    
    def test_text_complexity(self):
        """Test text complexity calculation."""
        text = "This is simple text. Very short sentences."
        result = get_text_complexity(text)
        assert "complexity" in result
        assert result["complexity"] in ["simple", "moderate", "complex"]


# ==================== API Health Tests ====================

class TestHealthEndpoints:
    """Test health and info endpoints."""
    
    def test_health_check(self):
        """Test health check endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "service" in data
    
    def test_info_endpoint(self):
        """Test info endpoint."""
        response = client.get("/info")
        assert response.status_code == 200
        data = response.json()
        assert "service" in data
        assert "features" in data
        assert "model" in data


# ==================== API Text Processing Tests ====================

class TestTextProcessingEndpoints:
    """Test text processing endpoints."""
    
    def test_humanize_endpoint_valid(self):
        """Test humanize endpoint with valid input."""
        response = client.post("/humanize", json={
            "text": "This is a sample text that needs to be humanized by the API."
        })
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "original" in data
        assert "humanized" in data
    
    def test_humanize_endpoint_invalid(self):
        """Test humanize endpoint with invalid input."""
        response = client.post("/humanize", json={
            "text": "short"
        })
        assert response.status_code in [400, 422]
    
    def test_analyze_endpoint(self):
        """Test text analysis endpoint."""
        response = client.post("/analyze", json={
            "text": "This is a test sentence for analysis. It has multiple words and structure."
        })
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "statistics" in data
        assert "character_count" in data["statistics"]
        assert "word_count" in data["statistics"]
        assert "sentence_count" in data["statistics"]


# ==================== Function Tests ====================

class TestHumanizeFunction:
    """Test humanize_text function."""
    
    def test_humanize_valid_input(self):
        """Test humanize with valid input."""
        text = "This is artificial intelligence text that sounds robotic and formulaic."
        result = humanize_text(text)
        assert result["success"] is True
        assert "humanized" in result
    
    def test_humanize_invalid_input(self):
        """Test humanize with invalid input."""
        result = humanize_text("")
        assert result["success"] is False
        assert "error" in result


class TestImproveFunction:
    """Test improve_text function."""
    
    def test_improve_valid_input(self):
        """Test improve with valid input."""
        text = "This text has errors. It need improement. The structure is bad."
        result = improve_text(text)
        assert result["success"] is True
        assert "improved" in result


class TestSummarizeFunction:
    """Test summarize_text function."""
    
    def test_summarize_valid_input(self):
        """Test summarize with valid input."""
        text = """This is a long text that contains multiple sentences. 
        Each sentence provides information about the topic. 
        The purpose is to show how summarization works. 
        This process reduces the length while keeping key information."""
        result = summarize_text(text)
        assert result["success"] is True
        assert "summary" in result
        assert result["compression_ratio"] <= 1.0


class TestToneAdjustFunction:
    """Test adjust_tone function."""
    
    def test_adjust_tone_professional(self):
        """Test tone adjustment to professional."""
        text = "Hey, this is a cool new feature that works pretty well."
        result = adjust_tone(text, "professional")
        assert result["success"] is True
        assert "adjusted" in result
        assert result["tone"] == "professional"
    
    def test_adjust_tone_casual(self):
        """Test tone adjustment to casual."""
        text = "The implementation was conducted to address the identified requirements."
        result = adjust_tone(text, "casual")
        assert result["success"] is True
        assert result["tone"] == "casual"
    
    def test_adjust_tone_invalid(self):
        """Test tone adjustment with invalid tone."""
        text = "This is a test text that is long enough."
        result = adjust_tone(text, "invalid_tone")
        assert result["success"] is False


class TestDetectorFunction:
    """Test detect_ai_text and parsing functions."""
    
    def test_parse_ai_detection_ai_text(self):
        """Test AI detection parsing for AI-generated text."""
        response = "This text appears to be AI-generated with 85% confidence"
        result = parse_ai_detection(response)
        assert result is True
    
    def test_parse_ai_detection_human_text(self):
        """Test AI detection parsing for human text."""
        response = "Verdict: Human-written. This looks like genuine human writing."
        result = parse_ai_detection(response)
        assert result is False
    
    def test_extract_confidence_with_percentage(self):
        """Test confidence extraction."""
        response = "Confidence: 85% that this is AI-generated"
        confidence = extract_confidence(response)
        assert confidence == 85
    
    def test_extract_confidence_no_percentage(self):
        """Test confidence extraction with no percentage."""
        response = "Unable to determine confidence level"
        confidence = extract_confidence(response)
        assert confidence == 0


# ==================== Integration Tests ====================

class TestIntegration:
    """Integration tests for complete workflows."""
    
    def test_full_pipeline_with_valid_text(self):
        """Test full processing pipeline with valid text."""
        text = """Artificial intelligence systems have demonstrated significant capabilities in various domains. 
        These systems process large amounts of data and generate insights. 
        The applications range from natural language processing to computer vision."""
        
        # Validate
        is_valid, _ = validate_text(text)
        assert is_valid is True
        
        # Analyze
        response = client.post("/analyze", json={"text": text})
        assert response.status_code == 200
        assert response.json()["success"] is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])