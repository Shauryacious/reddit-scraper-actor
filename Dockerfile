FROM apify/actor-python:3.11

# Copy requirements
COPY requirements.txt ./

# Install dependencies
# All listed packages (apify, aiohttp, pytest*) have pre-built wheels
# for both amd64 and arm64, so build tools are not needed
# Using pip as-is from base image (no upgrade needed for compatibility)
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . ./

# Run the actor
CMD python main.py
