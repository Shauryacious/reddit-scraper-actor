"""
Configuration constants for Reddit Scraper Actor
"""

# Reddit API Configuration
# Use old.reddit.com as it's more reliable for JSON API access
REDDIT_BASE_URL = "https://old.reddit.com"
# Use a realistic browser User-Agent to avoid 403 errors
REDDIT_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# API Limits
MAX_POSTS_PER_REQUEST = 100
MAX_COMMENTS_PER_REQUEST = 100

# Default Values
DEFAULT_SORT = "new"
DEFAULT_TIME_FILTER = "day"
DEFAULT_LIMIT = 25
DEFAULT_MAX_COMMENTS = 10

# Valid Options
VALID_SORT_OPTIONS = ["new", "hot", "top", "rising"]
VALID_TIME_FILTERS = ["hour", "day", "week", "month", "year", "all"]

# Rate Limiting
DELAY_BETWEEN_SUBREDDITS_SECONDS = 1.0
