"""
Main FastAPI application for AI Humanizer.
Provides REST API endpoints for text processing and AI detection.
"""
import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List
from config import settings
from humanizer import humanize_text, improve_text, summarize_text, adjust_tone, batch_humanize
from detector import detect_ai_text, get_ai_indicators
from utils import validate_text, count_words, count_sentences

# Configure logging
logging.basicConfig(
    level=settings.log_level,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="AI Humanizer API",
    description="Convert AI-generated text to human-like writing with advanced text processing features",
    version="1.0.0"
)

# Parse CORS origins from settings
cors_origins = settings.cors_origins.split(",") if isinstance(settings.cors_origins, str) else settings.cors_origins

# Add CORS middleware with configurable origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


# ==================== Pydantic Models ====================

class TextRequest(BaseModel):
    """Base model for text requests."""
    text: str = Field(..., min_length=10, max_length=10000, description="Text to process")


class HumanizeRequest(TextRequest):
    """Request model for humanize endpoint."""
    pass


class DetectRequest(TextRequest):
    """Request model for detect endpoint."""
    pass


class ImproveRequest(TextRequest):
    """Request model for improve endpoint."""
    pass


class SummarizeRequest(TextRequest):
    """Request model for summarize endpoint."""
    pass


class ToneRequest(TextRequest):
    """Request model for tone adjustment."""
    tone: str = Field(..., description="Desired tone: professional, casual, formal, friendly, persuasive, technical")


class BatchHumanizeRequest(BaseModel):
    """Request model for batch humanize."""
    texts: List[str] = Field(..., description="List of texts to humanize")


# ==================== Health & Info Endpoints ====================

@app.get("/", tags=["Health"])
def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "AI Humanizer API",
        "version": "1.0.0",
        "model": settings.ollama_model
    }


@app.get("/info", tags=["Info"])
def get_info():
    """Get API information and available features."""
    return {
        "service": "AI Humanizer API",
        "version": "1.0.0",
        "description": "Advanced text processing and AI detection service",
        "features": [
            "Text Humanization",
            "AI Detection",
            "Text Improvement",
            "Text Summarization",
            "Tone Adjustment",
            "Batch Processing",
            "Text Analysis"
        ],
        "model": settings.ollama_model,
        "config": {
            "max_text_length": settings.max_text_length,
            "min_text_length": settings.min_text_length,
            "request_timeout": settings.request_timeout
        }
    }


# ==================== Humanization Endpoints ====================

@app.post("/humanize", tags=["Text Processing"])
def humanize(request: HumanizeRequest):
    """
    Convert AI-generated text to sound naturally human-written.
    
    - **text**: The AI-generated text to humanize (10-10000 characters)
    
    Returns humanized text with metadata.
    """
    logger.info(f"Humanize request received (length: {len(request.text)})")
    
    try:
        result = humanize_text(request.text)
        
        if result["success"]:
            logger.info("Humanization successful")
            return {
                "success": True,
                "original": result["original"],
                "humanized": result["humanized"],
                "model": result["model"],
                "statistics": {
                    "original_length": len(result["original"]),
                    "humanized_length": result["char_count"],
                    "word_count": result["word_count"]
                }
            }
        else:
            raise HTTPException(status_code=400, detail=result["error"])
    except Exception as e:
        logger.error(f"Humanization error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/batch-humanize", tags=["Text Processing"])
def batch_humanize_endpoint(request: BatchHumanizeRequest):
    """
    Humanize multiple texts in batch.
    
    - **texts**: List of texts to humanize
    
    Returns list of humanized results.
    """
    logger.info(f"Batch humanize request received (count: {len(request.texts)})")
    
    try:
        results = batch_humanize(request.texts)
        
        return {
            "success": True,
            "count": len(results),
            "results": results
        }
    except Exception as e:
        logger.error(f"Batch humanization error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ==================== AI Detection Endpoints ====================

@app.post("/detect", tags=["AI Detection"])
def detect(request: DetectRequest):
    """
    Detect if text is likely AI-generated.
    
    - **text**: The text to analyze (10-10000 characters)
    
    Returns detection results with confidence score and analysis.
    """
    logger.info(f"Detection request received (length: {len(request.text)})")
    
    try:
        result = detect_ai_text(request.text)
        
        if result["success"]:
            logger.info(f"Detection successful (confidence: {result['confidence']}%)")
            return {
                "success": True,
                "is_ai_generated": result["is_ai"],
                "confidence": result["confidence"],
                "analysis": result["analysis"],
                "indicators": get_ai_indicators(request.text)
            }
        else:
            raise HTTPException(status_code=400, detail=result["error"])
    except Exception as e:
        logger.error(f"Detection error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ==================== Text Enhancement Endpoints ====================

@app.post("/improve", tags=["Text Processing"])
def improve(request: ImproveRequest):
    """
    Improve text for clarity, grammar, and professionalism.
    
    - **text**: The text to improve (10-10000 characters)
    
    Returns improved text with enhanced clarity and flow.
    """
    logger.info(f"Improve request received (length: {len(request.text)})")
    
    try:
        result = improve_text(request.text)
        
        if result["success"]:
            logger.info("Improvement successful")
            return {
                "success": True,
                "original": result["original"],
                "improved": result["improved"],
                "model": result["model"]
            }
        else:
            raise HTTPException(status_code=400, detail=result["error"])
    except Exception as e:
        logger.error(f"Improve error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/summarize", tags=["Text Processing"])
def summarize(request: SummarizeRequest):
    """
    Summarize text concisely while retaining key information.
    
    - **text**: The text to summarize (10-10000 characters)
    
    Returns condensed summary (~30% of original length).
    """
    logger.info(f"Summarize request received (length: {len(request.text)})")
    
    try:
        result = summarize_text(request.text)
        
        if result["success"]:
            logger.info(f"Summarization successful (compression: {result['compression_ratio']:.2%})")
            return {
                "success": True,
                "original": result["original"],
                "original_length": result["original_length"],
                "summary": result["summary"],
                "summary_length": result["summary_length"],
                "compression_ratio": result["compression_ratio"],
                "model": result["model"]
            }
        else:
            raise HTTPException(status_code=400, detail=result["error"])
    except Exception as e:
        logger.error(f"Summarize error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/adjust-tone", tags=["Text Processing"])
def adjust_tone_endpoint(request: ToneRequest):
    """
    Adjust text tone to match desired style.
    
    - **text**: The text to adjust (10-10000 characters)
    - **tone**: Desired tone (professional, casual, formal, friendly, persuasive, technical)
    
    Returns text rewritten in the specified tone.
    """
    logger.info(f"Tone adjustment request received (tone: {request.tone}, length: {len(request.text)})")
    
    try:
        result = adjust_tone(request.text, request.tone)
        
        if result["success"]:
            logger.info(f"Tone adjustment successful")
            return {
                "success": True,
                "original": result["original"],
                "adjusted": result["adjusted"],
                "tone": result["tone"],
                "model": result["model"]
            }
        else:
            raise HTTPException(status_code=400, detail=result["error"])
    except Exception as e:
        logger.error(f"Tone adjustment error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ==================== Text Analysis Endpoints ====================

@app.post("/analyze", tags=["Text Analysis"])
def analyze(request: TextRequest):
    """
    Analyze text for statistics and characteristics.
    
    - **text**: The text to analyze (10-10000 characters)
    
    Returns detailed text statistics.
    """
    logger.info(f"Analysis request received (length: {len(request.text)})")
    
    try:
        is_valid, error_msg = validate_text(request.text)
        if not is_valid:
            raise HTTPException(status_code=400, detail=error_msg)
        
        text = request.text.strip()
        word_count = count_words(text)
        sentence_count = count_sentences(text)
        
        # Safely calculate averages to avoid division by zero
        avg_word_length = (sum(len(w) for w in text.split()) / word_count) if word_count > 0 else 0
        avg_sentence_length = (word_count / sentence_count) if sentence_count > 0 else 0
        
        return {
            "success": True,
            "statistics": {
                "character_count": len(text),
                "word_count": word_count,
                "sentence_count": sentence_count,
                "average_word_length": round(avg_word_length, 2),
                "average_sentence_length": round(avg_sentence_length, 2)
            }
        }
    except Exception as e:
        logger.error(f"Analysis error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ==================== Startup & Shutdown ====================

@app.on_event("startup")
async def startup_event():
    """Startup event handler."""
    logger.info(f"AI Humanizer API starting up (model: {settings.ollama_model})")


@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event handler."""
    logger.info("AI Humanizer API shutting down")


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )