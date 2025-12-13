FROM apify/actor-python:3.11

# Copy requirements
COPY requirements.txt ./

# Install dependencies
# Upgrade pip and setuptools first to ensure compatibility with cross-platform builds
# This is especially important when building for multiple architectures (amd64/arm64)
# All listed packages (apify, aiohttp, pytest*) have pre-built wheels
# for both amd64 and arm64, so build tools are not needed
# pip automatically prefers wheels over source builds, which avoids cross-compilation issues
RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . ./

# Run the actor
CMD python main.py
