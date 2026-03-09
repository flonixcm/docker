# syntax=docker/dockerfile:1.7
FROM python:3.12-alpine

# Create non-root user for security
RUN addgroup -S app && adduser -S app -G app

# Set working directory
WORKDIR /app

# Install wget for healthcheck
RUN apk add --no-cache wget

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

# Create logs directory and set permissions
RUN mkdir -p /var/log/app && chown -R app:app /var/log/app

# Switch to non-root user
USER app

# Expose application port
EXPOSE 8080

# Healthcheck definition
HEALTHCHECK --interval=10s --timeout=3s --retries=5 \
  CMD wget -qO- http://localhost:8080/health >/dev/null || exit 1

# Start the application using Uvicorn
CMD ["python", "app.py"]