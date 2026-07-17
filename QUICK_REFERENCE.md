# AI Humanizer - Quick Reference Guide

## 🚀 Quick Start

### Installation (1 minute)
```bash
bash setup.sh
source venv/bin/activate
```

### Run Application
```bash
# Start Ollama
ollama serve

# In another terminal, start API
python app.py

# Visit API docs
open http://localhost:8000/docs
```

### Using Docker
```bash
docker-compose up
# Available at http://localhost:8000
```

---

## 📡 API Quick Reference

### 1. Health Check
```bash
GET /
```
Returns API status.

### 2. Humanize Text
```bash
POST /humanize
{
  "text": "Your AI-generated text here..."
}
```
**Response**: Original and humanized text with statistics.

### 3. Detect AI Text
```bash
POST /detect
{
  "text": "Text to analyze..."
}
```
**Response**: AI detection result with confidence score (0-100%).

### 4. Improve Text
```bash
POST /improve
{
  "text": "Text to improve..."
}
```
**Response**: Enhanced text with better grammar and clarity.

### 5. Summarize Text
```bash
POST /summarize
{
  "text": "Long text to summarize..."
}
```
**Response**: Concise summary (~30% of original length).

### 6. Adjust Tone
```bash
POST /adjust-tone
{
  "text": "Your text here...",
  "tone": "professional"
}
```
**Available tones**: professional, casual, formal, friendly, persuasive, technical

### 7. Batch Humanize
```bash
POST /batch-humanize
{
  "texts": ["text1...", "text2...", "text3..."]
}
```
**Response**: Array of humanized results.

### 8. Analyze Text
```bash
POST /analyze
{
  "text": "Your text here..."
}
```
**Response**: Character count, word count, sentence count, averages.

### 9. Get Info
```bash
GET /info
```
Returns available features and configuration.

---

## ⚙️ Configuration

### Environment Variables (.env)
```env
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama2
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True
LOG_LEVEL=INFO
MAX_TEXT_LENGTH=10000
MIN_TEXT_LENGTH=10
REQUEST_TIMEOUT=60
```

---

## 🧪 Testing

```bash
# Run all tests
pytest test_app.py -v

# Run specific test
pytest test_app.py::TestHumanizeFunction -v

# Run with coverage
pytest test_app.py --cov
```

---

## 📂 Project Files

| File | Purpose |
|------|---------|
| `app.py` | Main FastAPI application |
| `config.py` | Configuration management |
| `humanizer.py` | Text humanization logic |
| `detector.py` | AI detection logic |
| `prompts.py` | LLM prompt templates |
| `utils.py` | Utility functions |
| `test_app.py` | Test suite |
| `requirements.txt` | Python dependencies |
| `Dockerfile` | Container configuration |
| `docker-compose.yml` | Multi-container setup |
| `README.md` | Full documentation |
| `.env.example` | Configuration template |

---

## 🔍 Common Use Cases

### Use Case 1: Humanize AI Content
```bash
curl -X POST "http://localhost:8000/humanize" \
  -H "Content-Type: application/json" \
  -d '{"text": "The implementation of the system resulted in improved metrics."}'
```

### Use Case 2: Check if Text is AI-Generated
```bash
curl -X POST "http://localhost:8000/detect" \
  -H "Content-Type: application/json" \
  -d '{"text": "In contemporary discourse, artificial intelligence has emerged..."}'
```

### Use Case 3: Make Text More Professional
```bash
curl -X POST "http://localhost:8000/adjust-tone" \
  -H "Content-Type: application/json" \
  -d '{"text": "Hey, check this cool feature!", "tone": "professional"}'
```

### Use Case 4: Summarize Long Content
```bash
curl -X POST "http://localhost:8000/summarize" \
  -H "Content-Type: application/json" \
  -d '{"text": "Long article text here..."}'
```

### Use Case 5: Process Multiple Texts
```bash
curl -X POST "http://localhost:8000/batch-humanize" \
  -H "Content-Type: application/json" \
  -d '{"texts": ["text1...", "text2...", "text3..."]}'
```

---

## 🆘 Troubleshooting

### Problem: "Connection refused" on port 11434
**Solution**: Start Ollama with `ollama serve`

### Problem: Model not found
**Solution**: Pull model with `ollama pull llama2`

### Problem: Port 8000 already in use
**Solution**: Change port in .env or use: `python app.py --port 9000`

### Problem: Out of memory
**Solution**: Use lighter model or increase system RAM

### Problem: Text length error
**Solution**: Text must be 10-10000 characters. Check MAX_TEXT_LENGTH in .env

---

## 📊 Response Formats

### Success Response
```json
{
  "success": true,
  "original": "...",
  "humanized": "...",
  "model": "llama2",
  "statistics": {
    "original_length": 150,
    "humanized_length": 145,
    "word_count": 25
  }
}
```

### Error Response
```json
{
  "success": false,
  "error": "Text must be at least 10 characters",
  "status_code": 400
}
```

### Detection Response
```json
{
  "success": true,
  "is_ai_generated": true,
  "confidence": 85,
  "analysis": "...",
  "indicators": ["Formal transition patterns", "Long sentences"]
}
```

---

## 🐳 Docker Commands

```bash
# Build image
docker build -t ai-humanizer .

# Run container
docker run -p 8000:8000 ai-humanizer

# Using Docker Compose
docker-compose up
docker-compose down
docker-compose logs -f

# View running containers
docker ps

# Stop container
docker stop <container_id>
```

---

## 📦 Dependencies

**Required**:
- Python 3.8+
- Ollama (local LLM)

**Python Packages**:
- fastapi>=0.104
- uvicorn>=0.24
- pydantic>=2.5
- ollama>=0.1
- python-dotenv>=1.0

---

## 🔗 Important Links

- **Repository**: https://github.com/reyy56000-afk/ai-humanizer
- **API Docs**: http://localhost:8000/docs (when running)
- **Ollama**: https://ollama.ai
- **FastAPI**: https://fastapi.tiangolo.com

---

## ⚡ Performance Tips

1. **Batch Processing**: Use `/batch-humanize` for multiple texts
2. **Lighter Models**: Use `llama2` instead of larger models for speed
3. **Caching**: Implement caching for repeated requests
4. **Parallel**: Deploy multiple API instances with load balancing
5. **Timeout**: Adjust REQUEST_TIMEOUT based on model size

---

## 🎯 Common Patterns

### Pattern 1: Detect then Humanize
```bash
# First detect if AI-generated
curl -X POST "http://localhost:8000/detect" -d '{"text": "..."}'

# If AI-generated, humanize it
curl -X POST "http://localhost:8000/humanize" -d '{"text": "..."}'
```

### Pattern 2: Improve then Summarize
```bash
# Improve text quality
curl -X POST "http://localhost:8000/improve" -d '{"text": "..."}'

# Then summarize
curl -X POST "http://localhost:8000/summarize" -d '{"text": "..."}'
```

### Pattern 3: Analyze and Adjust
```bash
# Analyze current text
curl -X POST "http://localhost:8000/analyze" -d '{"text": "..."}'

# Adjust tone based on analysis
curl -X POST "http://localhost:8000/adjust-tone" -d '{"text": "...", "tone": "professional"}'
```

---

## 📞 Support

- **Issues**: https://github.com/reyy56000-afk/ai-humanizer/issues
- **Discussions**: https://github.com/reyy56000-afk/ai-humanizer/discussions
- **Email**: reyy56000@gmail.com

---

## ✅ Verification Checklist

After setup, verify everything works:

- [ ] Ollama is running
- [ ] Python virtual environment activated
- [ ] Dependencies installed (`pip list`)
- [ ] API starts without errors
- [ ] Can access http://localhost:8000/docs
- [ ] Health check returns 200
- [ ] Can make test request to /humanize
- [ ] Tests pass (`pytest test_app.py`)

---

## 🎓 Learning Path

1. **Start Here**: Read README.md
2. **Explore**: Visit http://localhost:8000/docs
3. **Try Examples**: Use curl commands from this guide
4. **Understand Code**: Review app.py and modules
5. **Contribute**: See CONTRIBUTING.md
6. **Deploy**: Use docker-compose for production

---

**Last Updated**: July 17, 2026 | **Version**: 1.0.0
