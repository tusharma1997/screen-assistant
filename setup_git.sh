#!/bin/bash
# Script to initialize git and prepare for GitHub upload

echo "🔧 Setting up Git repository..."
echo ""

# Initialize git repository
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Screen Context GPT Assistant"

echo ""
echo "✅ Git repository initialized!"
echo ""
echo "📝 Next steps to upload to GitHub:"
echo ""
echo "1. Create a new repository on GitHub:"
echo "   - Go to https://github.com/new"
echo "   - Name it 'screen-assistant' (or your preferred name)"
echo "   - Don't initialize with README, .gitignore, or license (we already have them)"
echo ""
echo "2. Connect your local repository to GitHub:"
echo "   git remote add origin https://github.com/YOUR_USERNAME/screen-assistant.git"
echo ""
echo "3. Push to GitHub:"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "Or if you prefer SSH:"
echo "   git remote add origin git@github.com:YOUR_USERNAME/screen-assistant.git"
echo "   git push -u origin main"
echo ""

