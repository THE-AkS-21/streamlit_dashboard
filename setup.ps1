Write-Host "🔧 Creating virtual environment..."
python -m venv venv

Write-Host "✅ Activating virtual environment..."
& .\venv\Scripts\Activate.ps1

Write-Host "📦 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

Write-Host "🚀 Setup complete. To activate next time, run:"
Write-Host ".\venv\Scripts\Activate.ps1"
