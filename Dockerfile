# Build stage for dependencies
FROM python:3.8-slim-buster AS builder

WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt && \
    pip install --no-cache-dir gunicorn

# Production stage
FROM python:3.8-slim-buster AS production

WORKDIR /app

# Copy dependencies from builder
COPY --from=builder /root/.local /root/.local

# Copy application code
COPY app.py .

# Create a non-root user for security
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Set environment variables for production
ENV PATH=/root/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    GUNICORN_CMD_ARGS="--workers=4 --threads=2 --timeout=60 --graceful-timeout=30 --keep-alive=5 --max-requests=1000 --max-requests-jitter=50 --bind=0.0.0.0:8000 --access-logfile=- --error-logfile=-"

# Expose port 8000 (non-root)
EXPOSE 8000

# Run with Gunicorn
CMD ["gunicorn", "app:app"]