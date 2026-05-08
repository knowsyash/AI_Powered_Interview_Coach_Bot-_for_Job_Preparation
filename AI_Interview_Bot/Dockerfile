# Dockerfile for Hugging Face Spaces (Flask app)
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Download NLTK data at build time
RUN python -m nltk.downloader punkt stopwords wordnet omw-1.4

# Expose the port Hugging Face expects
EXPOSE 7860

# Run the Flask app on the correct port
CMD ["python", "app.py"]
