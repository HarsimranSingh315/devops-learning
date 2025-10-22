# ============================================
# Stage 1: Builder
# ============================================
FROM python:3.9-alpine AS builder

# Install build dependencies for psycopg2
RUN apk add --no-cache gcc musl-dev postgresql-dev

WORKDIR /app

# Install Python dependencies (without --user flag)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ============================================
# Stage 2: Runtime - Alpine based
# ============================================
FROM python:3.9-alpine

# Install only runtime libraries (not build tools)
RUN apk add --no-cache libpq

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages

# Copy application
COPY app.py .

# Create non-root user and change ownership
RUN addgroup -S appuser && adduser -S appuser -G appuser && \
    chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

EXPOSE 5000

# Simplified health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health').read()" || exit 1

CMD ["python", "app.py"]
