FROM apify/actor-python:3.11

# Install system dependencies needed for building Python packages
# (especially important for cross-platform builds)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip to latest version for better cross-platform support
RUN pip install --upgrade pip setuptools wheel

# Copy requirements
COPY requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . ./

# Run the actor
CMD python main.py
