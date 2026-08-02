# Use a lightweight Python image
FROM python:3.12-slim

# Prevent Python from writing .pyc files and buffer stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy requirements first for better Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Cloud Run provides the PORT environment variable
ENV PORT=8080

# Expose the port
EXPOSE 8080

# Start the Flask app with Gunicorn
CMD exec gunicorn --bind :$PORT app:app