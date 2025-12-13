"""
Helper utility functions for Reddit Scraper Actor
"""

from typing import List, Dict, Any
from datetime import datetime, timezone


def clean_subreddit_name(subreddit: str) -> str:
    """
    Clean subreddit name by removing r/ prefix if present
    
    Args:
        subreddit: Subreddit name (with or without r/ prefix)
        
    Returns:
        Cleaned subreddit name without r/ prefix
    """
    return subreddit.strip().lstrip("r/")


def format_timestamp(utc_timestamp: float) -> str:
    """
    Convert UTC timestamp to ISO format string
    
    Args:
        utc_timestamp: Unix timestamp in UTC
        
    Returns:
        ISO format datetime string
    """
    return datetime.fromtimestamp(utc_timestamp, tz=timezone.utc).isoformat()


def validate_input(input_data: Dict[str, Any]) -> None:
    """
    Validate input parameters
    
    Args:
        input_data: Input dictionary from Apify
        
    Raises:
        ValueError: If input validation fails
    """
    subreddits = input_data.get("subreddits", [])
    search_query = input_data.get("searchQuery", "")
    
    if not subreddits and not search_query:
        raise ValueError("Either 'subreddits' or 'searchQuery' must be provided")
    
    sort_by = input_data.get("sortBy", "new")
    if sort_by not in ["new", "hot", "top", "rising"]:
        raise ValueError(f"Invalid sortBy: {sort_by}. Must be one of: new, hot, top, rising")
    
    limit = input_data.get("limit", 25)
    if not isinstance(limit, int) or limit < 1 or limit > 100:
        raise ValueError("limit must be an integer between 1 and 100")


def normalize_post_data(post_data: Dict, source_type: str, source_name: str) -> Dict:
    """
    Normalize Reddit post data to consistent format
    
    Args:
        post_data: Raw post data from Reddit API
        source_type: Type of source (subreddit, search)
        source_name: Name of source (subreddit name or search query)
        
    Returns:
        Normalized post dictionary
    """
    return {
        "id": post_data.get("id", ""),
        "title": post_data.get("title", ""),
        "selftext": post_data.get("selftext", ""),
        "author": post_data.get("author", "[deleted]"),
        "subreddit": post_data.get("subreddit", source_name),
        "score": post_data.get("score", 0),
        "upvote_ratio": post_data.get("upvote_ratio", 0),
        "num_comments": post_data.get("num_comments", 0),
        "created_utc": post_data.get("created_utc", 0),
        "created_at": format_timestamp(post_data.get("created_utc", 0)),
        "url": post_data.get("url", ""),
        "permalink": f"https://reddit.com{post_data.get('permalink', '')}",
        "is_self": post_data.get("is_self", False),
        "is_video": post_data.get("is_video", False),
        "thumbnail": post_data.get("thumbnail", ""),
        "domain": post_data.get("domain", ""),
        "source_type": source_type,
        "source_name": source_name,
    }


def normalize_comment_data(comment_data: Dict, post_id: str) -> Dict:
    """
    Normalize Reddit comment data to consistent format
    
    Args:
        comment_data: Raw comment data from Reddit API
        post_id: ID of the parent post
        
    Returns:
        Normalized comment dictionary
    """
    return {
        "id": comment_data.get("id", ""),
        "author": comment_data.get("author", "[deleted]"),
        "body": comment_data.get("body", ""),
        "score": comment_data.get("score", 0),
        "created_utc": comment_data.get("created_utc", 0),
        "created_at": format_timestamp(comment_data.get("created_utc", 0)),
        "permalink": f"https://reddit.com{comment_data.get('permalink', '')}",
        "is_submitter": comment_data.get("is_submitter", False),
        "parent_id": comment_data.get("parent_id", ""),
        "post_id": post_id,
    }

