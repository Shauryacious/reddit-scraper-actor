# Output Format Reference

## Overview

The Reddit Scraper Actor outputs data in multiple formats:
1. **Dataset (JSON)** - Default Apify dataset with structured post data
2. **CSV Export** - CSV files in the key-value store for easy data analysis
3. **Output Schema** - Configured output schema for proper display in Apify Console

Each item in the dataset represents a Reddit post, optionally including comments.

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

## CSV Export Format

The actor automatically generates CSV files in the key-value store for easy data analysis and export.

### Posts-Only CSV (`reddit_scraper_output.csv`)

This CSV file is **always generated** and contains all scraped posts with the following columns:

- `id` - Reddit post ID
- `title` - Post title
- `selftext` - Post body text
- `author` - Post author username
- `subreddit` - Subreddit name
- `score` - Post score
- `upvote_ratio` - Upvote ratio (0.0 to 1.0)
- `num_comments` - Number of comments
- `created_utc` - Unix timestamp
- `created_at` - ISO 8601 formatted timestamp
- `url` - Post URL
- `permalink` - Reddit permalink
- `is_self` - Boolean (true/false)
- `is_video` - Boolean (true/false)
- `thumbnail` - Thumbnail image URL
- `domain` - Domain of linked URL
- `source_type` - Source type (subreddit or search)
- `source_name` - Subreddit name or search query

### CSV with Comments (`reddit_scraper_output_with_comments.csv`)

This CSV file is **generated when `includeComments` is `true`** and contains posts with comments as separate rows. Each comment row includes:

**Post columns (repeated for each comment):**
- `post_id`, `post_title`, `post_selftext`, `post_author`, `subreddit`, `post_score`, `upvote_ratio`, `num_comments`, `post_created_utc`, `post_created_at`, `post_url`, `post_permalink`, `is_self`, `is_video`, `thumbnail`, `domain`, `source_type`, `source_name`

**Comment columns:**
- `comment_id` - Comment ID
- `comment_author` - Comment author username
- `comment_body` - Comment text
- `comment_score` - Comment score
- `comment_created_utc` - Unix timestamp
- `comment_created_at` - ISO 8601 formatted timestamp
- `comment_permalink` - Reddit permalink to comment
- `is_submitter` - Boolean (true/false)
- `row_type` - Either "post" or "comment"

**Note:** Posts without comments will appear as a single row with empty comment fields. Posts with comments will have one row for the post and additional rows for each comment.

### CSV Format Details

- **Encoding**: UTF-8
- **Delimiter**: Comma (,)
- **Quoting**: Proper CSV escaping for special characters, newlines, and commas
- **Boolean values**: Converted to lowercase strings ("true"/"false")
- **Empty values**: Empty strings for missing/null values

## Output Schema Configuration

The actor uses Apify's output schema to organize and display outputs in the Apify Console. The output schema defines:

1. **Reddit Posts** - Link to the default dataset containing all scraped posts
2. **CSV Export** - Link to the posts-only CSV file
3. **CSV Export (with Comments)** - Link to the CSV file with comments (when available)

The output schema is defined in `.actor/output_schema.json` and uses Apify's template variables to generate proper URLs at runtime.

### Accessing Outputs

**Via Apify Console:**
- Navigate to the run's **Output** tab
- Click on any output to view/download the data

**Via API:**
The `GET Run` API endpoint includes an `output` property with URLs to all outputs:

```json
{
  "output": {
    "posts": "https://api.apify.com/v2/datasets/<dataset-id>/items",
    "csvExport": "https://api.apify.com/v2/key-value-stores/<store-id>/records/reddit_scraper_output.csv",
    "csvExportWithComments": "https://api.apify.com/v2/key-value-stores/<store-id>/records/reddit_scraper_output_with_comments.csv"
  }
}
```

## Rate Limiting Notes

- Reddit API limits: 100 posts per request, 100 comments per request
- The actor respects rate limits with delays between requests
- Some fields may be missing for deleted or removed content

