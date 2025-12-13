# Reddit Scraper Actor

A powerful Apify actor that scrapes Reddit posts, comments, and threads from subreddits using Reddit's public API. No authentication required. Challenge-compliant for the Apify $1M Challenge.

## Features

- ✅ **No Authentication Required** - Uses Reddit's public JSON API
- ✅ **Multiple Subreddits** - Scrape multiple subreddits in one run
- ✅ **Search Functionality** - Search Reddit for posts matching a query
- ✅ **Comments Support** - Optionally scrape comments for each post
- ✅ **Flexible Sorting** - Sort by new, hot, top, or rising
- ✅ **Time Filters** - Filter top posts by time period (hour, day, week, month, year, all)
- ✅ **Challenge Compliant** - Reddit is allowed in the Apify $1M Challenge

## Input

The actor accepts the following input parameters:

### Required
- At least one of:
  - `subreddits` (array): List of subreddits to scrape
  - `searchQuery` (string): Search query to find posts

### Optional
- `sortBy` (string): How to sort posts - `new`, `hot`, `top`, or `rising` (default: `new`)
- `timeFilter` (string): Time period for 'top' sorted posts - `hour`, `day`, `week`, `month`, `year`, `all` (default: `day`)
- `limit` (integer): Maximum number of posts per subreddit (1-100, default: 25)
- `includeComments` (boolean): Whether to scrape comments for each post (default: `false`)
- `maxCommentsPerPost` (integer): Maximum comments per post if includeComments is true (1-100, default: 10)

## Input Schema Example

```json
{
  "subreddits": ["programming", "r/technology", "webdev"],
  "sortBy": "hot",
  "limit": 50,
  "includeComments": true,
  "maxCommentsPerPost": 20
}
```

Or with search:

```json
{
  "searchQuery": "python programming",
  "sortBy": "new",
  "limit": 25
}
```

## Output

The actor outputs data to the default dataset. Each post includes:

```json
{
  "id": "abc123",
  "title": "Post Title",
  "selftext": "Post content/body text",
  "author": "username",
  "subreddit": "programming",
  "score": 1234,
  "upvote_ratio": 0.95,
  "num_comments": 42,
  "created_utc": 1234567890,
  "created_at": "2024-01-01T00:00:00.000Z",
  "url": "https://example.com",
  "permalink": "https://reddit.com/r/programming/comments/abc123/title",
  "is_self": false,
  "is_video": false,
  "thumbnail": "https://...",
  "domain": "example.com",
  "source_type": "subreddit",
  "source_name": "programming",
  "comments": [
    {
      "id": "comment123",
      "author": "commenter",
      "body": "Comment text",
      "score": 10,
      "created_utc": 1234567890,
      "created_at": "2024-01-01T00:00:00.000Z",
      "permalink": "https://reddit.com/r/programming/comments/abc123/title/comment123",
      "is_submitter": false
    }
  ]
}
```

## Usage Examples

### Example 1: Scrape a single subreddit

```json
{
  "subreddits": ["programming"],
  "sortBy": "hot",
  "limit": 50
}
```

### Example 2: Scrape multiple subreddits

```json
{
  "subreddits": ["programming", "technology", "webdev"],
  "sortBy": "new",
  "limit": 25
}
```

### Example 3: Search Reddit

```json
{
  "searchQuery": "machine learning",
  "sortBy": "top",
  "timeFilter": "week",
  "limit": 100
}
```

### Example 4: Scrape with comments

```json
{
  "subreddits": ["AskReddit"],
  "sortBy": "hot",
  "limit": 10,
  "includeComments": true,
  "maxCommentsPerPost": 20
}
```

## Rate Limiting

Reddit's public API has rate limits. The actor includes delays between requests to be respectful. For high-volume scraping, consider:
- Using multiple actor runs
- Increasing delays between subreddits
- Respecting Reddit's terms of service

## Limitations

- Maximum 100 posts per subreddit per request (Reddit API limit)
- Maximum 100 comments per post per request (Reddit API limit)
- Rate limiting may apply for high-volume scraping
- Some subreddits may be private or restricted

## Technical Details

- **Language**: Python 3.11
- **Runtime**: Apify Actor platform
- **API**: Reddit JSON API (public, no authentication)
- **Dependencies**: Apify SDK, aiohttp
- **Architecture**: Modular structure with separate services and utilities
- **Code Quality**: Black formatting, flake8 linting, isort import sorting
- **Testing**: pytest with coverage reporting

## Project Structure

```
reddit-scraper-actor/
├── src/
│   ├── main.py                 # Main entry point
│   ├── config.py               # Configuration constants
│   ├── services/
│   │   └── reddit_service.py  # Reddit API service
│   └── utils/
│       └── helpers.py          # Utility functions
├── tests/                      # Unit tests
├── documentation/             # Comprehensive documentation
│   ├── getting-started/       # Setup guides
│   ├── deployment/            # CI/CD guides
│   ├── api-reference/         # API documentation
│   └── learnings/             # Development insights
├── .actor/
│   └── actor.json             # Actor configuration
├── input_schema.json          # Input schema
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Docker configuration
└── README.md                  # This file
```

## Development

### Code Formatting

This project uses [Black](https://black.readthedocs.io/) for code formatting. Before committing, run:

```bash
black src/ tests/
```

The CI/CD pipeline enforces code formatting standards. See [Code Formatting Guide](./documentation/development/code-formatting.md) for details.

### Running Tests

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=src --cov-report=term-missing
```

### Linting

```bash
# Format code
black src/ tests/

# Sort imports
isort src/ tests/

# Lint code
flake8 src/ tests/
```

## Documentation

Comprehensive documentation is available in the [`documentation/`](./documentation/) directory:

- **[Getting Started](./documentation/getting-started/)** - Setup and installation guides
- **[Deployment](./documentation/deployment/)** - CI/CD and deployment documentation
- **[Development](./documentation/development/)** - Code formatting and development guidelines
- **[API Reference](./documentation/api-reference/)** - Input/output specifications
- **[Learnings](./documentation/learnings/)** - Development insights and best practices

See the [Documentation Index](./documentation/README.md) for a complete overview.

## Based On

This actor is based on the TradeX Reddit service implementation, adapted for the Apify platform with a modular Python structure following Apify actor best practices.

## Challenge Compliance

✅ **Apify $1M Challenge Compliant**
- Reddit is not in the excluded platforms list
- Uses public API (no authentication required)
- Respects rate limits and terms of service

## Support

For issues, questions, or contributions, please refer to the Apify documentation or create an issue in the repository.

## License

ISC

