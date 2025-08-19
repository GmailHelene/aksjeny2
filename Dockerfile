# Use Python 3.10 slim as base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Configure apt to retry downloads
RUN echo 'Acquire::Retries "3";' > /etc/apt/apt.conf.d/80-retries

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    build-essential \
    wget \
    pkg-config \
    git \
    make \
    automake \
    autoconf \
    libtool \
    libssl-dev \
    python3-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create ta-lib.conf for ldconfig
RUN echo "/usr/lib" > /etc/ld.so.conf.d/ta-lib.conf

# Copy requirements and installation scripts
COPY requirements.txt install_talib.sh ./
RUN chmod +x install_talib.sh

# Install Python dependencies first
RUN pip install --upgrade pip && \
    pip install --no-cache-dir numpy==1.23.5 Cython==0.29.36

# Install TA-Lib
RUN ./install_talib.sh

# Install remaining requirements
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV FLASK_ENV=production
ENV PYTHONPATH=/app
ENV TA_LIBRARY_PATH=/usr/lib
ENV TA_INCLUDE_PATH=/usr/include/ta-lib

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash app && chown -R app:app /app
USER app

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=10s --retries=3 CMD curl -f http://localhost:5000/health || exit 1

# Run the application
CMD ["python3", "main.py"]
