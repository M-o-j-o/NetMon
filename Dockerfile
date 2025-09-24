FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for agent and service management
RUN apt-get update && \
    apt-get install -y gcc python3-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files (including agent and scripts)
COPY . .

EXPOSE 5000

# Run the Flask app by default
CMD ["python", "app.py"]
