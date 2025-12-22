FROM python:3.11-slim

WORKDIR /stock

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/stock

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose port
EXPOSE 8000

# Change to stock directory and run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]