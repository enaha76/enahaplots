#!/bin/bash
# Backend setup script

echo "🚀 Setting up enahaplots backend..."

# Create virtual environment
python3 -m venv venv
echo "✅ Created virtual environment"

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt
echo "✅ Installed dependencies"

# Install enahaplots library
pip install -e ..
echo "✅ Installed enahaplots library"

echo ""
echo "🎉 Setup complete!"
echo ""
echo "To start the server:"
echo "  source venv/bin/activate"
echo "  uvicorn main:app --reload"
