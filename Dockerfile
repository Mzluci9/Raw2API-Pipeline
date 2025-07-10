# Use official Python slim image for smaller size
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Command to keep container running (will be overridden in docker-compose)
CMD ["tail", "-f", "/dev/null"]