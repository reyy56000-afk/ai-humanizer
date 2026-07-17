#!/bin/bash

# AI Humanizer Setup Script

echo "🚀 AI Humanizer Setup"
echo "===================="

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    exit 1
fi

echo "✅ Python 3 found"

# Check Ollama
if ! command -v ollama &> /dev/null; then
    echo "⚠️  Ollama not found. Please install Ollama from https://ollama.ai"
    echo "   After installation, run: ollama serve"
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Copy environment file
if [ ! -f .env ]; then
    echo "⚙️  Creating .env file..."
    cp .env.example .env
    echo "   Configure .env with your settings"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Make sure Ollama is running: ollama serve"
echo "2. Pull a model: ollama pull llama2"
echo "3. Activate environment: source venv/bin/activate"
echo "4. Start the API: python app.py"
echo "5. Visit: http://localhost:8000/docs"
echo ""
