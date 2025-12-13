# Async Context Managers - Key Learnings

## Problem Encountered

During test development, we encountered the error:
```
'coroutine' object does not support the asynchronous context manager protocol
```

This occurred when mocking `aiohttp.ClientSession().get()` in unit tests.

## Root Cause

The issue was in how we were mocking async context managers. In Python's `aiohttp` library:

1. `ClientSession()` returns an async context manager
2. `session.get()` also returns an async context manager (the HTTP response)
3. Both need to be properly mocked with `__aenter__` and `__aexit__` methods

## Incorrect Approach

```python
# ❌ This doesn't work
async def mock_get(*args, **kwargs):
    return mock_response

mock_get.__aenter__ = AsyncMock(return_value=mock_response)
mock_get.__aexit__ = AsyncMock(return_value=None)

mock_session.get = mock_get  # Function, not an async context manager
```

The problem: `mock_get` is a function, not an object that can be used with `async with`.

## Correct Approach

```python
# ✅ This works
mock_get_context = AsyncMock()
mock_get_context.__aenter__ = AsyncMock(return_value=mock_response)
mock_get_context.__aexit__ = AsyncMock(return_value=None)

mock_session = AsyncMock()
mock_session.get = MagicMock(return_value=mock_get_context)  # Returns context manager
mock_session.__aenter__ = AsyncMock(return_value=mock_session)
mock_session.__aexit__ = AsyncMock(return_value=None)
```

## Key Insights

### 1. Async Context Managers Must Be Objects

Async context managers must be objects (not functions) that implement:
- `__aenter__()` - Returns the value used in `async with`
- `__aexit__()` - Handles cleanup

### 2. Mocking Pattern

When mocking nested async context managers:
1. Create a mock object for the inner context manager (e.g., `mock_get_context`)
2. Set `__aenter__` and `__aexit__` on that object
3. Make the parent method return that object using `MagicMock(return_value=...)`

### 3. Why MagicMock?

`MagicMock` is used for `session.get` because:
- It's a regular method call (not async)
- It needs to return an async context manager object
- `MagicMock(return_value=...)` ensures it returns our mock context manager

## Real-World Code Pattern

In `reddit_service.py`:

```python
async with aiohttp.ClientSession() as session:  # Outer context manager
    async with session.get(url, headers=self.headers) as response:  # Inner context manager
        data = await response.json()
```

Both `ClientSession()` and `session.get()` are async context managers that need proper mocking.

## Testing Best Practices

1. **Mock at the right level**: Mock `aiohttp.ClientSession` class, not individual instances
2. **Use AsyncMock for async methods**: Methods like `response.json()` need `AsyncMock`
3. **Create proper context managers**: Don't try to make functions into context managers
4. **Test both success and error paths**: Mock different response statuses

## Related Concepts

- **Context Managers**: Objects that manage resources with `with` statements
- **Async Context Managers**: Same concept but for async code with `async with`
- **Protocol**: Python's structural typing - objects that implement `__aenter__` and `__aexit__` are async context managers

## References

- [Python Async Context Managers](https://docs.python.org/3/reference/datamodel.html#asynchronous-context-managers)
- [aiohttp Documentation](https://docs.aiohttp.org/)
- [pytest-asyncio](https://pytest-asyncio.readthedocs.io/)

