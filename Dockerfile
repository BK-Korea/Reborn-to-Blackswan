FROM python:3.11-slim

WORKDIR /stock

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/stock

# Install Node.js for frontend build
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs gcc \
    && apt-get clean

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

# Copy frontend and install dependencies
COPY frontend/ ./frontend/
RUN cd frontend && npm install

# Build frontend
RUN cd frontend && npm run build

# Copy the rest of the application code
COPY . .

# Expose port
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]