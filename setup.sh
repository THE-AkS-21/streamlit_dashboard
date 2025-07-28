#!/bin/bash

echo "🔧 Creating virtual environment..."
python3 -m venv venv

echo "✅ Activating virtual environment..."
source venv/bin/activate

echo "📦 Installing dependencies from requirements.txt..."
pip install --upgrade pip
pip install -r requirements.txt

echo "🚀 Setup complete. To activate the environment next time, run:"
echo "source venv/bin/activate"
