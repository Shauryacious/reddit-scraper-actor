# Output Format Reference

## Overview

The Reddit Scraper Actor outputs data to the default Apify dataset. Each item in the dataset represents a Reddit post, optionally including comments.

## Post Object Structure

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
  "source_name": "programming"
}
```

## Field Descriptions

### Core Fields

- **`id`** (string): Reddit post ID
- **`title`** (string): Post title
- **`selftext`** (string): Post body text (empty for link posts)
- **`author`** (string): Post author username
- **`subreddit`** (string): Subreddit name (without r/ prefix)

### Engagement Metrics

- **`score`** (integer): Post score (upvotes - downvotes)
- **`upvote_ratio`** (float): Ratio of upvotes (0.0 to 1.0)
- **`num_comments`** (integer): Number of comments

### Timestamps

- **`created_utc`** (integer): Unix timestamp in UTC
- **`created_at`** (string): ISO 8601 formatted timestamp

### URL Fields

- **`url`** (string): External URL (for link posts) or self post URL
- **`permalink`** (string): Full Reddit permalink
- **`domain`** (string): Domain of linked URL (for link posts)

### Metadata

- **`is_self`** (boolean): Whether post is a self/text post
- **`is_video`** (boolean): Whether post contains a video
- **`thumbnail`** (string): Thumbnail image URL
- **`source_type`** (string): Source type - `"subreddit"` or `"search"`
- **`source_name`** (string): Subreddit name or search query

## Comments Array

When `includeComments` is `true`, each post includes a `comments` array:

```json
{
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

### Comment Fields

- **`id`** (string): Comment ID
- **`author`** (string): Comment author username
- **`body`** (string): Comment text
- **`score`** (integer): Comment score
- **`created_utc`** (integer): Unix timestamp in UTC
- **`created_at`** (string): ISO 8601 formatted timestamp
- **`permalink`** (string): Full Reddit permalink to comment
- **`is_submitter`** (boolean): Whether commenter is the post author

## Summary Statistics

The actor also stores summary statistics in the key-value store:

```json
{
  "totalPosts": 150,
  "subredditsScraped": 3,
  "searchQuery": null,
  "timestamp": "2024-01-01T00:00:00.000Z"
}
```

## Data Normalization

All data is normalized to ensure consistency:
- Subreddit names are cleaned (r/ prefix removed)
- Timestamps are converted to ISO 8601 format
- Missing fields are handled gracefully
- Deleted comments are filtered out

## Rate Limiting Notes

- Reddit API limits: 100 posts per request, 100 comments per request
- The actor respects rate limits with delays between requests
- Some fields may be missing for deleted or removed content

