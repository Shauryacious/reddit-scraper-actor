# Apify Actor Development - Key Learnings

## Overview

This document captures key learnings from developing a Reddit Scraper Actor for the Apify platform.

## Apify Actor Architecture

### Core Components

1. **Main Entry Point** (`main.py`)
   - Manages Actor lifecycle
   - Handles input/output
   - Coordinates scraping logic

2. **Services** (`src/services/`)
   - Business logic for external APIs
   - Isolated, testable components

3. **Utilities** (`src/utils/`)
   - Helper functions
   - Data normalization
   - Input validation

4. **Configuration** (`src/config.py`)
   - Constants and defaults
   - Centralized configuration

## Apify SDK Patterns

### Actor Context Manager

```python
from apify import Actor

async def main():
    async with Actor:
        # Actor code here
        input_data = await Actor.get_input()
        # Process data
        await Actor.push_data(result)
```

### Key Actor Methods

- `Actor.get_input()`: Get input data
- `Actor.push_data(item)`: Add item to dataset
- `Actor.set_value(key, value)`: Store in key-value store
- `Actor.get_value(key)`: Retrieve from key-value store
- `Actor.log.info/warning/error()`: Logging
- `Actor.fail(exit_code)`: Fail the actor run

### Input Schema

Define input schema in `input_schema.json`:

```json
{
  "title": "Reddit Scraper Input",
  "type": "object",
  "properties": {
    "subreddits": {
      "type": "array",
      "items": {"type": "string"}
    }
  }
}
```

## Project Structure Best Practices

### Recommended Structure

```
actor/
├── src/
│   ├── __init__.py
│   ├── main.py          # Main entry point
│   ├── config.py         # Configuration
│   ├── services/         # External service integrations
│   └── utils/            # Utility functions
├── tests/                # Test files
├── .actor/               # Actor metadata
│   └── actor.json
├── input_schema.json     # Input schema
├── requirements.txt      # Python dependencies
├── Dockerfile           # Container definition
└── README.md            # Documentation
```

### Separation of Concerns

- **Services**: Handle external API interactions
- **Utils**: Pure functions, no side effects
- **Main**: Orchestration and Actor SDK usage
- **Config**: Centralized constants

## Docker Configuration

### Dockerfile Best Practices

```dockerfile
FROM apify/actor-python:3.11

# Copy requirements first (caching)
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Copy source code
COPY src/ ./src/
COPY main.py ./

# Set entry point
CMD ["python", "main.py"]
```

### Multi-stage Builds

For optimization, use multi-stage builds when needed.

### Multi-Architecture Docker Builds

When building Docker images for multiple architectures (AMD64 and ARM64), you may encounter QEMU emulation issues.

#### Common Issue: "Invalid ELF image for this architecture"

**Error Message:**
```
process "/dev/.buildkit_qemu_emulator /bin/bash -o pipefail -c pip install..." 
did not complete successfully: exit code: 255
```

**Root Cause:**
- QEMU emulation not properly configured for cross-platform builds
- Base image may not support all target architectures
- Build process attempting to execute binaries for wrong architecture

#### Solution: Configure QEMU in CI/CD

**GitHub Actions Workflow Setup:**

```yaml
steps:
  - name: Set up QEMU for multi-architecture builds
    uses: docker/setup-qemu-action@v3
    with:
      platforms: arm64
  
  - name: Set up Docker Buildx
    uses: docker/setup-buildx-action@v3
  
  - name: Build and push Docker image
    uses: docker/build-push-action@v6
    with:
      platforms: linux/amd64,linux/arm64
```

#### Best Practices

1. **Start with Single Architecture**: Build for `linux/amd64` first to verify Dockerfile works
2. **Add QEMU Setup**: Always set up QEMU before Buildx when targeting multiple platforms
3. **Verify Base Image Support**: Ensure base image (`apify/actor-python:3.11`) supports target architectures
4. **Use Wheel-Only Installs**: Ensure pip prefers pre-built wheels to avoid cross-compilation issues

#### Dockerfile Optimization for Multi-Arch

```dockerfile
FROM apify/actor-python:3.11

# Copy requirements first (caching)
COPY requirements.txt ./

# Install dependencies
# pip automatically prefers wheels over source builds
# This avoids cross-compilation issues in multi-arch builds
RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . ./

# Set entry point
CMD python main.py
```

#### Troubleshooting Multi-Arch Builds

1. **If ARM64 build fails**: Start with AMD64 only, verify base image supports ARM64
2. **QEMU errors**: Ensure QEMU setup step comes before Buildx setup
3. **Package installation failures**: Check if packages have pre-built wheels for target architecture
4. **Build timeout**: Multi-arch builds take longer; consider building platforms separately if needed

## Testing Apify Actors

### Local Testing

Create `run_local.py` for local testing:

```python
import asyncio
from apify import Actor
from src.main import run_scraper

async def main():
    # Mock Actor context
    with open('test-input.json') as f:
        input_data = json.load(f)
    
    await run_scraper(input_data)

if __name__ == "__main__":
    asyncio.run(main())
```

### Testing with Apify CLI

```bash
apify run
```

## CI/CD Integration

### GitHub Actions Workflows

1. **CI Workflow**: Run tests on every push
2. **CD Workflow**: Build and push Docker images
3. **Docker Build Test**: Verify Docker builds on PRs

### Docker Hub Integration

- Build multi-platform images (amd64, arm64)
- Tag with version numbers
- Push to Docker Hub for Apify to use

**Important**: When setting up multi-architecture builds, ensure QEMU is configured before Buildx. See the [Multi-Architecture Docker Builds](#multi-architecture-docker-builds) section above for details.

## Error Handling

### Best Practices

1. **Log Errors**: Use `Actor.log.error()` for failures
2. **Graceful Degradation**: Return partial results when possible
3. **Fail Explicitly**: Use `Actor.fail()` for fatal errors
4. **Validate Input**: Check input early and fail fast

### Example

```python
try:
    posts = await reddit_service.get_posts_from_subreddit(...)
except Exception as e:
    Actor.log.error(f"Error fetching posts: {e}")
    return []  # Return empty list, don't fail entire run
```

## Rate Limiting

### Handling Rate Limits

1. **Add Delays**: Use `asyncio.sleep()` between requests
2. **Respect Limits**: Don't exceed API rate limits
3. **Retry Logic**: Implement exponential backoff for retries

```python
await asyncio.sleep(DELAY_BETWEEN_SUBREDDITS_SECONDS)
```

## Data Normalization

### Why Normalize?

- Consistent output format
- Handle missing fields gracefully
- Clean subreddit names (remove r/ prefix)
- Convert timestamps to ISO format

### Example

```python
def normalize_post_data(post_data, source_type, source_name):
    return {
        "id": post_data.get("id", ""),
        "title": post_data.get("title", ""),
        "created_at": format_timestamp(post_data.get("created_utc", 0)),
        "source_type": source_type,
        "source_name": source_name,
    }
```

## Logging

### Log Levels

- `Actor.log.info()`: General information
- `Actor.log.debug()`: Detailed debugging info
- `Actor.log.warning()`: Warnings (non-fatal)
- `Actor.log.error()`: Errors

### Structured Logging

```python
Actor.log.info("Scraping subreddit", {
    "subreddit": subreddit,
    "limit": limit,
    "sort": sort
})
```

## Performance Considerations

1. **Async Operations**: Use `async/await` for I/O operations
2. **Batch Processing**: Process multiple items efficiently
3. **Memory Management**: Don't load all data into memory
4. **Connection Pooling**: Reuse HTTP connections

## Security Best Practices

1. **No Secrets in Code**: Use Apify secrets/environment variables
2. **Input Validation**: Validate all user input
3. **Rate Limiting**: Respect API rate limits
4. **Error Messages**: Don't expose sensitive info in errors

## Deployment Checklist

- [ ] All tests passing
- [ ] Docker image builds successfully
- [ ] Input schema defined
- [ ] README updated
- [ ] Secrets configured in Apify
- [ ] CI/CD pipeline working
- [ ] Error handling tested
- [ ] Logging in place

## Common Issues and Solutions

### Issue: Actor fails to start

**Solution**: Check `main.py` entry point and Dockerfile CMD

### Issue: Input not received

**Solution**: Verify `input_schema.json` and `Actor.get_input()` usage

### Issue: Data not saved

**Solution**: Ensure `Actor.push_data()` is called correctly

### Issue: Docker build fails

**Solution**: Check Dockerfile syntax and dependencies

### Issue: Multi-architecture Docker build fails with "Invalid ELF image" error

**Error**: 
```
process "/dev/.buildkit_qemu_emulator /bin/bash..." did not complete successfully: exit code: 255
```

**Solution**: 
1. Ensure QEMU is set up before Buildx in your CI/CD workflow
2. Add `docker/setup-qemu-action@v3` step before `docker/setup-buildx-action@v3`
3. Start with single architecture (`linux/amd64`) to verify Dockerfile works
4. Verify base image supports target architectures
5. See [Multi-Architecture Docker Builds](#multi-architecture-docker-builds) section for detailed solution

## Resources

- [Apify Actor Documentation](https://docs.apify.com/actors)
- [Apify Python SDK](https://docs.apify.com/sdk/python)
- [Apify CLI](https://docs.apify.com/cli)

