FROM python:3.12-slim

WORKDIR /app

# Prevent pip caching and handle large package downloads over slow or flaky connections
ENV PIP_DEFAULT_TIMEOUT=3000 \
    PIP_RETRIES=10

COPY requirements.txt .
RUN pip install --no-cache-dir \
    --default-timeout=3000 \
    --retries 10 \
    -r requirements.txt

# Copy application files and sample documentation
COPY . .

# Pre-populate ChromaDB vector store during build
RUN python ingest.py

# Expose FastAPI service port
EXPOSE 8000

# Start Uvicorn bound to 0.0.0.0
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
