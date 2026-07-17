"""
Test suite for AI Humanizer application.
Contains unit tests for all major functions.
"""
import pytest
from fastapi.testclient import TestClient
from app import app
from humanizer import humanize_text, improve_text, summarize_text, adjust_tone
from detector import detect_ai_text
from utils import validate_text, count_words, count_sentences, sanitize_text


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
    
    def test_count_sentences(self):
        """Test sentence counting."""
        text = "This is a test. This is another. And one more!"
        assert count_sentences(text) == 3


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


# ==================== Function Tests ====================

class TestHumanizeFunction:
    """Test humanize_text function."""
    
    def test_humanize_valid_input(self):
        """Test humanize with valid input."""
        text = "This is artificial intelligence text that sounds robotic."
        result = humanize_text(text)
        assert result["success"] is True
        assert "humanized" in result
        assert result["original"] == text
    
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
        assert result["compression_ratio"] < 1.0


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
        text = "This is a test text."
        result = adjust_tone(text, "invalid_tone")
        assert result["success"] is False


class TestDetectorFunction:
    """Test detect_ai_text function."""
    
    def test_detect_ai_text(self):
        """Test AI text detection."""
        text = "In contemporary discourse, artificial intelligence has emerged as a transformative paradigm."
        result = detect_ai_text(text)
        assert result["success"] is True
        assert "is_ai" in result
        assert "confidence" in result
        assert isinstance(result["confidence"], int)


# ==================== Integration Tests ====================

class TestIntegration:
    """Integration tests for complete workflows."""
    
    def test_humanize_detect_workflow(self):
        """Test humanize followed by detection workflow."""
        original_text = "The implementation of the system was designed to optimize performance metrics."
        
        # Humanize
        humanize_result = humanize_text(original_text)
        assert humanize_result["success"] is True
        
        # Detect on humanized text
        humanized = humanize_result["humanized"]
        detect_result = detect_ai_text(humanized)
        assert detect_result["success"] is True
    
    def test_full_processing_pipeline(self):
        """Test full processing pipeline."""
        text = """Artificial intelligence systems have demonstrated significant capabilities in various domains. 
        These systems process large amounts of data and generate insights. 
        The applications range from natural language processing to computer vision."""
        
        # Analyze
        is_valid, _ = validate_text(text)
        assert is_valid is True
        
        # Humanize
        humanize_result = humanize_text(text)
        assert humanize_result["success"] is True
        
        # Improve
        improve_result = improve_text(humanize_result["humanized"])
        assert improve_result["success"] is True
        
        # Summarize
        summarize_result = summarize_text(improve_result["improved"])
        assert summarize_result["success"] is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
