# Use lightweight and modern Python image
FROM python:3.11-slim

# Environment variables for cleaner output and faster startup
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system-level dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy Python dependencies first (for better Docker layer caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy application code
COPY . .

# Expose default Streamlit port
EXPOSE 8501

# Health check for container status
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Entrypoint command to run Streamlit app (customize your entry file if needed)
CMD ["streamlit", "run", "main.py", \
     "--server.port=8501", \
     "--server.address=0.0.0.0", \
     "--server.headless=true", \
     "--server.enableCORS=false", \
     "--server.enableXsrfProtection=false"]
