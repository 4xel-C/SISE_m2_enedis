# Use Python 3.13 slim image as base
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install UV package manager
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies using UV
RUN uv sync --frozen --no-dev

# Copy application code
COPY . .

# Expose ports for Streamlit and FastAPI
EXPOSE 8501 8000

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Create a startup script to run both services
RUN echo '#!/bin/bash\n\
    mkdir -p .streamlit\n\
    echo "MAPBOX_API_KEY = \"${MAPBOX_API_KEY}\"" > .streamlit/secrets.toml\n\
    uv run uvicorn backend.main:app --host 0.0.0.0 --port 8000 &\n\
    uv run streamlit run home.py\n\
    wait' > /app/start.sh && chmod +x /app/start.sh

# Run the application
CMD ["/app/start.sh"]