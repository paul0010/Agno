# Use Python 3.11 slim image for smaller size
FROM python:3.11-slim

# Set working directory
WORKDIR /code

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Copy requirements file
COPY ./requirements.txt /code/requirements.txt

# Install dependencies
# First upgrade pip and install google-genai explicitly to avoid dependency conflicts
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir google-genai && \
    pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy application code
COPY ./agno_agent.py /code/agno_agent.py

# Create directory for database
RUN mkdir -p /code/data

# Expose port
EXPOSE 8000

# Run the FastAPI application with uvicorn
# Using 4 workers for better performance
# Add --proxy-headers for Dokploy's Traefik integration
CMD ["uvicorn", "agno_agent:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4", "--proxy-headers"]
