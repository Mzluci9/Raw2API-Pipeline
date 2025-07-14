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
# CMD ["tail", "-f", "/dev/null"]



# Install build dependencies and system libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gcc \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python packages
RUN pip install --upgrade pip

# Copy the rest of the application


# Define default command (update this with your app entry point)
CMD ["python", "your_entry_script.py"]
