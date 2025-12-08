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

# Use waitress - pure Python WSGI server that handles real-time updates properly
CMD waitress-serve --port=$PORT --threads=4 app_wealth_inequality:server

