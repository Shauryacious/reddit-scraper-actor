"""
Configuration constants for Reddit Scraper Actor
"""

# Reddit API Configuration
REDDIT_BASE_URL = "https://www.reddit.com"
REDDIT_USER_AGENT = "RedditScraper/1.0 (Apify Actor)"

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

