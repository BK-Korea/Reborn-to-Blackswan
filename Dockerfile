FROM python:3.11-slim

WORKDIR /stock

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/stock

# Install system dependencies
RUN apt-get update && \
    apt-get install -y curl && \
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs gcc && \
    apt-get clean

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

# Copy frontend and install dependencies with cache busting
COPY frontend/package*.json ./frontend/
RUN cd frontend && rm -rf .next node_modules package-lock.json && npm install

# Copy frontend source code
COPY frontend/ ./frontend/

# Build frontend - Next.js static export
RUN cd frontend && npm run build

# Copy the rest of the application code
COPY . .

# Expose port
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]