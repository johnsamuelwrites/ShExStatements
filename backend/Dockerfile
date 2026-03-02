# ShExStatements Backend Dockerfile
# Optimized production image for FastAPI application

FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash appuser

# Install shared shexstatements package from repository root
COPY setup.py README.md requirements.txt shexstatements.sh ./
COPY shexstatements/ ./shexstatements/
RUN pip install --no-cache-dir .

# Install backend API package
COPY backend/pyproject.toml ./backend/pyproject.toml
COPY backend/api/ ./backend/api/
RUN pip install --no-cache-dir -e ./backend --no-deps

# Clean build dependencies
RUN apt-get purge -y gcc && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

# Set ownership
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/api/v1/health')" || exit 1

# Run the application
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
