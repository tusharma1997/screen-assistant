#!/bin/bash
# Installation script for Screen Context GPT Assistant

echo "🚀 Installing Screen Context GPT Assistant..."
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
REQUIRED_VERSION="3.8"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "❌ Python 3.8 or higher is required. You have Python $PYTHON_VERSION"
    exit 1
fi

echo "✅ Python $PYTHON_VERSION found"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo ""
echo "✅ Dependencies installed successfully!"
echo ""

# Check for .env file
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from template..."
    if [ -f .env.example ]; then
        cp .env.example .env
        echo "📝 Please edit .env and add your OPENAI_API_KEY"
    else
        echo "OPENAI_API_KEY=your_api_key_here" > .env
        echo "📝 Created .env file. Please edit it and add your OPENAI_API_KEY"
    fi
else
    echo "✅ .env file found"
fi

echo ""
echo "🎉 Installation complete!"
echo ""
echo "To run the GUI version:"
echo "  python3 screen_assistant_gui.py"
echo ""
echo "To run the CLI version:"
echo "  python3 screen_assistant.py"
echo ""

