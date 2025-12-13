# Input Schema Reference

## Overview

The Reddit Scraper Actor accepts JSON input with various parameters to control scraping behavior.

## Required Parameters

At least one of the following must be provided:

- **`subreddits`** (array of strings): List of subreddit names to scrape
- **`searchQuery`** (string): Search query to find posts across Reddit

## Optional Parameters

### `sortBy` (string)
How to sort posts. Valid options:
- `new` - Newest posts first (default)
- `hot` - Hot/popular posts
- `top` - Top posts (requires `timeFilter`)
- `rising` - Rising posts

**Default**: `new`

### `timeFilter` (string)
Time period for 'top' sorted posts. Valid options:
- `hour` - Last hour
- `day` - Last day (default)
- `week` - Last week
- `month` - Last month
- `year` - Last year
- `all` - All time

**Default**: `day`  
**Note**: Only used when `sortBy` is `top`

### `limit` (integer)
Maximum number of posts per subreddit or search result.

**Range**: 1-100  
**Default**: 25

### `includeComments` (boolean)
Whether to scrape comments for each post.

**Default**: `false`

### `maxCommentsPerPost` (integer)
Maximum number of comments to fetch per post when `includeComments` is `true`.

**Range**: 1-100  
**Default**: 10

## Input Examples

### Basic Subreddit Scraping

```json
{
  "subreddits": ["programming"],
  "sortBy": "hot",
  "limit": 50
}
```

### Multiple Subreddits

```json
{
  "subreddits": ["programming", "r/technology", "webdev"],
  "sortBy": "new",
  "limit": 25
}
```

### Search Query

```json
{
  "searchQuery": "python programming",
  "sortBy": "new",
  "limit": 25
}
```

### With Comments

```json
{
  "subreddits": ["AskReddit"],
  "sortBy": "hot",
  "limit": 10,
  "includeComments": true,
  "maxCommentsPerPost": 20
}
```

### Top Posts with Time Filter

```json
{
  "subreddits": ["programming"],
  "sortBy": "top",
  "timeFilter": "week",
  "limit": 100
}
```

## Validation Rules

- At least one of `subreddits` or `searchQuery` must be provided
- `sortBy` must be one of: `new`, `hot`, `top`, `rising`
- `timeFilter` must be one of: `hour`, `day`, `week`, `month`, `year`, `all`
- `limit` must be between 1 and 100
- `maxCommentsPerPost` must be between 1 and 100
- Subreddit names can include or exclude the `r/` prefix (e.g., `"programming"` or `"r/programming"`)

