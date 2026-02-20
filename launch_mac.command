#!/bin/bash
# ALFA CONVERTER Launcher for macOS

# Get the directory where the script is located
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

echo "🚀 Initializing Selenium to Playwright converter by local LLM..."

# Check for Python
if ! command -v python3 &> /dev/null
then
    echo "❌ Python 3 is not installed. Please install it to continue."
    exit 1
fi

# Check for Ollama
if ! command -v ollama &> /dev/null
then
    echo "❌ Ollama is not installed. Please install it and download 'codellama'."
    exit 1
fi

# Check if Flask is installed
python3 -c "import flask" &> /dev/null
if [ $? -ne 0 ]; then
    echo "📦 Installing dependencies (Flask, requests)..."
    pip3 install flask requests
fi

# Start Backend in background
echo "⚙️ Starting Backend Server..."
python3 app.py &
BACKEND_PID=$!

# Wait for server to start
sleep 2

# Open HTML Interface
echo "🌐 Opening UI..."
open http://localhost:5001

# Keep terminal open and handle shutdown
echo "✅ System running. Close this terminal or press Ctrl+C to stop."
trap "kill $BACKEND_PID; exit" INT TERM
wait
