FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose port (Railway uses PORT env var)
EXPOSE 8080

# Use gunicorn with gevent worker for real-time updates
# gevent handles concurrent connections properly for Dash interval callbacks
CMD gunicorn --worker-class gevent --workers 1 --bind 0.0.0.0:$PORT --timeout 120 app_wealth_inequality:server

