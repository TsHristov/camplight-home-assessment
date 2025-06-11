# Use Python 3.13 alpine image (5MB instead of 125MB for slim)
FROM python:3.13-alpine

WORKDIR /app

# Install dependencies
RUN apk add --no-cache \
    curl \
    gcc \
    musl-dev \
    python3-dev

# Copy requirements and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN addgroup -S appuser && adduser -S appuser -G appuser \
    && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]