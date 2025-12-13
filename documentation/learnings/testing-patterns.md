# Testing Patterns - Key Learnings

## Overview

This document covers testing patterns and best practices learned while developing the Reddit Scraper Actor.

## Test Structure

### Organization

```
tests/
├── __init__.py
├── test_helpers.py      # Unit tests for utility functions
└── test_reddit_service.py  # Unit tests for Reddit service
```

### Test Class Structure

```python
class TestRedditService:
    """Tests for RedditService class"""
    
    @pytest.fixture
    def reddit_service(self):
        """Create a RedditService instance for testing"""
        return RedditService()
    
    @pytest.mark.asyncio
    async def test_method_name(self, reddit_service):
        """Test description"""
        # Test implementation
```

## Key Testing Patterns

### 1. Fixtures for Test Setup

Use `@pytest.fixture` to create reusable test objects:

```python
@pytest.fixture
def reddit_service(self):
    """Create a RedditService instance for testing"""
    return RedditService()
```

Benefits:
- DRY (Don't Repeat Yourself)
- Consistent test setup
- Easy to modify test dependencies

### 2. Async Test Marking

Always mark async tests with `@pytest.mark.asyncio`:

```python
@pytest.mark.asyncio
async def test_async_method(self, reddit_service):
    result = await reddit_service.some_method()
    assert result == expected
```

### 3. Mocking External Dependencies

Use `unittest.mock.patch` to mock external dependencies:

```python
from unittest.mock import patch, AsyncMock, MagicMock

with patch("aiohttp.ClientSession", return_value=mock_session):
    result = await reddit_service.get_posts_from_subreddit(...)
```

**Key Points:**
- Patch at the import location, not the usage location
- Use `AsyncMock` for async methods
- Use `MagicMock` for regular methods that return objects

### 4. Testing Error Handling

Always test both success and error paths:

```python
def test_success_case(self, reddit_service):
    # Test successful operation
    pass

def test_error_case(self, reddit_service):
    # Test error handling
    pass
```

### 5. Testing Edge Cases

Test boundary conditions and edge cases:

```python
def test_empty_input(self, reddit_service):
    """Test with empty input"""
    result = await reddit_service.get_comments_for_post("abc", "test", 0)
    assert result == []

def test_max_limit(self, reddit_service):
    """Test with maximum limit"""
    result = await reddit_service.get_posts_from_subreddit("test", "new", "day", 100)
    assert len(result) <= 100
```

## Mocking Patterns

### Mocking HTTP Responses

```python
mock_response = AsyncMock()
mock_response.status = 200
mock_response.json = AsyncMock(return_value=mock_data)

mock_get_context = AsyncMock()
mock_get_context.__aenter__ = AsyncMock(return_value=mock_response)
mock_get_context.__aexit__ = AsyncMock(return_value=None)

mock_session = AsyncMock()
mock_session.get = MagicMock(return_value=mock_get_context)
```

### Mocking Async Context Managers

See [async-context-managers.md](./async-context-managers.md) for detailed explanation.

## Test Coverage

### Coverage Goals

- **Unit Tests**: Test individual functions/methods in isolation
- **Integration Tests**: Test component interactions (if applicable)
- **Edge Cases**: Test boundary conditions and error paths

### Running Tests with Coverage

```bash
pytest --cov=src --cov-report=html tests/
```

## Common Pitfalls

### 1. Forgetting `@pytest.mark.asyncio`

**Problem**: Async tests won't run properly
**Solution**: Always mark async tests

### 2. Incorrect Mock Setup

**Problem**: Mocks don't behave like real objects
**Solution**: Use `AsyncMock` for async methods, proper context manager setup

### 3. Testing Implementation Details

**Problem**: Tests break when refactoring
**Solution**: Test behavior, not implementation

### 4. Not Testing Error Cases

**Problem**: Code fails in production
**Solution**: Test both success and error paths

## Best Practices

1. **Test Names**: Use descriptive names that explain what is being tested
2. **Arrange-Act-Assert**: Structure tests clearly
3. **One Assertion Per Test**: Focus each test on one behavior
4. **Test Independence**: Tests should not depend on each other
5. **Fast Tests**: Keep tests fast to encourage frequent running

## Example: Complete Test

```python
@pytest.mark.asyncio
async def test_get_posts_from_subreddit_success(self, reddit_service):
    """Test successful post fetching"""
    # Arrange
    mock_response_data = {
        "data": {
            "children": [{"data": {...}}]
        }
    }
    
    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.json = AsyncMock(return_value=mock_response_data)
    
    mock_get_context = AsyncMock()
    mock_get_context.__aenter__ = AsyncMock(return_value=mock_response)
    mock_get_context.__aexit__ = AsyncMock(return_value=None)
    
    mock_session = AsyncMock()
    mock_session.get = MagicMock(return_value=mock_get_context)
    mock_session.__aenter__ = AsyncMock(return_value=mock_session)
    mock_session.__aexit__ = AsyncMock(return_value=None)
    
    # Act
    with patch("aiohttp.ClientSession", return_value=mock_session):
        posts = await reddit_service.get_posts_from_subreddit("python", "new", "day", 25)
    
    # Assert
    assert len(posts) == 1
    assert posts[0]["id"] == "test123"
```

## Tools and Libraries

- **pytest**: Testing framework
- **pytest-asyncio**: Async test support
- **pytest-cov**: Coverage reporting
- **unittest.mock**: Mocking framework

## References

- [pytest Documentation](https://docs.pytest.org/)
- [pytest-asyncio](https://pytest-asyncio.readthedocs.io/)
- [Python Testing Guide](https://docs.python.org/3/library/unittest.mock.html)

