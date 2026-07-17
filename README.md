# AI Humanizer

A comprehensive, production-ready REST API for converting AI-generated text to natural, human-like writing. Built with FastAPI, Ollama, and advanced NLP techniques.

## Features

🎯 **Core Features**
- ✨ **Text Humanization** - Convert AI-generated text to sound naturally human-written
- 🔍 **AI Detection** - Identify likely AI-generated content with confidence scoring
- 📝 **Text Improvement** - Enhance clarity, grammar, and professionalism
- 📊 **Summarization** - Create concise summaries while preserving key information
- 🎨 **Tone Adjustment** - Rewrite text in different tones (professional, casual, formal, etc.)
- 📈 **Batch Processing** - Process multiple texts efficiently
- 📋 **Text Analysis** - Detailed statistical analysis of text

## Tech Stack

- **Backend**: FastAPI 0.104+
- **Server**: Uvicorn
- **AI Model**: Ollama (Local LLM)
- **Validation**: Pydantic v2
- **Testing**: Pytest
- **Language**: Python 3.8+

## Installation

### Prerequisites
- Python 3.8 or higher
- Ollama (with llama2 or llama3.2 model)

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/reyy56000-afk/ai-humanizer.git
cd ai-humanizer
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your settings (optional)
```

5. **Start Ollama service**
```bash
ollama serve
```

6. **Run the application**
```bash
python app.py
```

The API will be available at `http://localhost:8000`

## API Documentation

### Interactive Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Endpoints

#### Health Check
```bash
GET /
```
Returns API status and health information.

#### Get Info
```bash
GET /info
```
Returns API features, configuration, and available endpoints.

#### Humanize Text
```bash
POST /humanize
```
Convert AI-generated text to human-like writing.

**Request:**
```json
{
  "text": "The implementation of the machine learning model resulted in significant performance improvements across multiple metrics."
}
```

**Response:**
```json
{
  "success": true,
  "original": "...",
  "humanized": "...",
  "model": "llama2",
  "statistics": {
    "original_length": 120,
    "humanized_length": 115,
    "word_count": 20
  }
}
```

#### Detect AI-Generated Text
```bash
POST /detect
```
Identify if text is likely AI-generated with confidence score.

**Request:**
```json
{
  "text": "In the contemporary landscape, artificial intelligence has emerged as a transformative paradigm..."
}
```

**Response:**
```json
{
  "success": true,
  "is_ai_generated": true,
  "confidence": 85,
  "analysis": "...",
  "indicators": ["Formal transition patterns", "High proportion of long sentences"]
}
```

#### Improve Text
```bash
POST /improve
```
Enhance text for clarity, grammar, and professionalism.

**Request:**
```json
{
  "text": "This text has some errors. It need better structure. Grammar is bad."
}
```

**Response:**
```json
{
  "success": true,
  "original": "...",
  "improved": "...",
  "model": "llama2"
}
```

#### Summarize Text
```bash
POST /summarize
```
Create concise summaries of longer texts.

**Request:**
```json
{
  "text": "Long text here with multiple paragraphs..."
}
```

**Response:**
```json
{
  "success": true,
  "original": "...",
  "summary": "...",
  "compression_ratio": 0.32,
  "model": "llama2"
}
```

#### Adjust Tone
```bash
POST /adjust-tone
```
Rewrite text in a specific tone.

**Request:**
```json
{
  "text": "Hey, check out this awesome new feature!",
  "tone": "professional"
}
```

**Response:**
```json
{
  "success": true,
  "original": "...",
  "adjusted": "...",
  "tone": "professional",
  "model": "llama2"
}
```

Available tones: `professional`, `casual`, `formal`, `friendly`, `persuasive`, `technical`

#### Analyze Text
```bash
POST /analyze
```
Get detailed text statistics and analysis.

**Request:**
```json
{
  "text": "Your text here for analysis."
}
```

**Response:**
```json
{
  "success": true,
  "statistics": {
    "character_count": 150,
    "word_count": 25,
    "sentence_count": 3,
    "average_word_length": 5.2,
    "average_sentence_length": 8.3
  }
}
```

#### Batch Humanize
```bash
POST /batch-humanize
```
Process multiple texts efficiently.

**Request:**
```json
{
  "texts": [
    "First AI-generated text...",
    "Second AI-generated text...",
    "Third AI-generated text..."
  ]
}
```

**Response:**
```json
{
  "success": true,
  "count": 3,
  "results": [
    { "success": true, "humanized": "..." },
    { "success": true, "humanized": "..." },
    { "success": true, "humanized": "..." }
  ]
}
```

## Configuration

Edit `.env` file to customize settings:

```env
# Ollama Configuration
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama2

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True
LOG_LEVEL=INFO

# Text Processing
MAX_TEXT_LENGTH=10000
MIN_TEXT_LENGTH=10
REQUEST_TIMEOUT=60
```

## Testing

Run the test suite:

```bash
pytest test_app.py -v
```

Run specific test class:

```bash
pytest test_app.py::TestUtilities -v
```

Run with coverage:

```bash
pytest test_app.py --cov=. --cov-report=html
```

## Project Structure

```
ai-humanizer/
├── app.py                 # Main FastAPI application
├── config.py             # Configuration management
├── humanizer.py          # Text humanization & enhancement
├── detector.py           # AI text detection
├── prompts.py            # LLM prompt templates
├── utils.py              # Utility functions
├── test_app.py           # Test suite
├── requirements.txt      # Python dependencies
├── .env.example          # Environment variables template
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

## Performance Tips

1. **Batch Processing**: Use `/batch-humanize` for multiple texts
2. **Caching**: Implement caching for repeated requests
3. **Model Selection**: Use lighter models (llama2) for faster responses
4. **Timeout Configuration**: Adjust REQUEST_TIMEOUT based on model size
5. **Parallel Processing**: Deploy multiple API instances with load balancing

## Error Handling

The API returns consistent error responses:

```json
{
  "success": false,
  "error": "Error description",
  "status_code": 400
}
```

Common status codes:
- `200` - Success
- `400` - Bad request (invalid input)
- `422` - Validation error
- `500` - Server error

## Security Considerations

- ✅ Input validation and sanitization
- ✅ Text length limits
- ✅ CORS support for cross-origin requests
- ✅ Error message sanitization
- ✅ Logging and monitoring ready

## Limitations

- Requires Ollama running locally
- Processing time depends on model size and text length
- Maximum text length: 10,000 characters (configurable)
- Model quality depends on selected LLM

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## License

This project is open source and available under the MIT License.

## Support

For issues, questions, or suggestions:
- 📧 Email: reyy56000@gmail.com
- 🐛 GitHub Issues: [Create an issue](https://github.com/reyy56000-afk/ai-humanizer/issues)
- 💬 Discussions: [Start a discussion](https://github.com/reyy56000-afk/ai-humanizer/discussions)

## Roadmap

- [ ] Add database support for history tracking
- [ ] Implement caching layer
- [ ] Add more language support
- [ ] Create web UI dashboard
- [ ] Add API authentication/authorization
- [ ] Implement rate limiting
- [ ] Add advanced analytics
- [ ] Create Docker deployment
- [ ] Add webhook support
- [ ] Performance optimization

## Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework
- [Ollama](https://ollama.ai/) - Local LLM framework
- [Pydantic](https://docs.pydantic.dev/) - Data validation

---

**Built with ❤️ by Geoffrey Getaro Maroa**

**Last Updated**: July 2026 | **Version**: 1.0.0
