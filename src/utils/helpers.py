"""
Helper utility functions for Reddit Scraper Actor
"""

import csv
import io
import json
from datetime import datetime, timezone
from typing import Any, Dict, List


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
        raise ValueError(
            f"Invalid sortBy: {sort_by}. Must be one of: new, hot, top, rising"
        )

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


def export_posts_to_csv(posts: List[Dict]) -> str:
    """
    Export posts to CSV format following Apify's standard format

    Args:
        posts: List of post dictionaries

    Returns:
        CSV string with all posts and comments
    """
    if not posts:
        return ""

    # Define CSV columns for posts
    post_columns = [
        "id",
        "title",
        "selftext",
        "author",
        "subreddit",
        "score",
        "upvote_ratio",
        "num_comments",
        "created_utc",
        "created_at",
        "url",
        "permalink",
        "is_self",
        "is_video",
        "thumbnail",
        "domain",
        "source_type",
        "source_name",
    ]

    # Create CSV in memory
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=post_columns, extrasaction="ignore")
    writer.writeheader()

    # Write posts
    for post in posts:
        # Create a copy of post without comments for the main row
        post_row = {k: v for k, v in post.items() if k != "comments"}
        
        # Convert boolean values to strings for CSV
        for key in ["is_self", "is_video"]:
            if key in post_row:
                post_row[key] = str(post_row[key]).lower()
        
        # Convert None values to empty strings
        for key in post_row:
            if post_row[key] is None:
                post_row[key] = ""
        
        writer.writerow(post_row)

    return output.getvalue()


def export_posts_with_comments_to_csv(posts: List[Dict]) -> str:
    """
    Export posts with comments to CSV format.
    Creates separate rows for each comment, with post data repeated.

    Args:
        posts: List of post dictionaries (may include comments)

    Returns:
        CSV string with posts and comments as separate rows
    """
    if not posts:
        return ""

    # Define CSV columns including comment fields
    columns = [
        "post_id",
        "post_title",
        "post_selftext",
        "post_author",
        "subreddit",
        "post_score",
        "upvote_ratio",
        "num_comments",
        "post_created_utc",
        "post_created_at",
        "post_url",
        "post_permalink",
        "is_self",
        "is_video",
        "thumbnail",
        "domain",
        "source_type",
        "source_name",
        "comment_id",
        "comment_author",
        "comment_body",
        "comment_score",
        "comment_created_utc",
        "comment_created_at",
        "comment_permalink",
        "is_submitter",
        "row_type",  # "post" or "comment"
    ]

    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=columns, extrasaction="ignore")
    writer.writeheader()

    for post in posts:
        # Prepare post data
        post_data = {
            "post_id": post.get("id", ""),
            "post_title": post.get("title", ""),
            "post_selftext": post.get("selftext", ""),
            "post_author": post.get("author", ""),
            "subreddit": post.get("subreddit", ""),
            "post_score": post.get("score", 0),
            "upvote_ratio": post.get("upvote_ratio", 0),
            "num_comments": post.get("num_comments", 0),
            "post_created_utc": post.get("created_utc", 0),
            "post_created_at": post.get("created_at", ""),
            "post_url": post.get("url", ""),
            "post_permalink": post.get("permalink", ""),
            "is_self": str(post.get("is_self", False)).lower(),
            "is_video": str(post.get("is_video", False)).lower(),
            "thumbnail": post.get("thumbnail", ""),
            "domain": post.get("domain", ""),
            "source_type": post.get("source_type", ""),
            "source_name": post.get("source_name", ""),
            "comment_id": "",
            "comment_author": "",
            "comment_body": "",
            "comment_score": "",
            "comment_created_utc": "",
            "comment_created_at": "",
            "comment_permalink": "",
            "is_submitter": "",
            "row_type": "post",
        }

        # Convert None values to empty strings
        for key in post_data:
            if post_data[key] is None:
                post_data[key] = ""

        # Write post row
        writer.writerow(post_data)

        # Write comment rows if comments exist
        comments = post.get("comments", [])
        if comments:
            for comment in comments:
                comment_row = post_data.copy()
                comment_row.update({
                    "comment_id": comment.get("id", ""),
                    "comment_author": comment.get("author", ""),
                    "comment_body": comment.get("body", ""),
                    "comment_score": comment.get("score", 0),
                    "comment_created_utc": comment.get("created_utc", 0),
                    "comment_created_at": comment.get("created_at", ""),
                    "comment_permalink": comment.get("permalink", ""),
                    "is_submitter": str(comment.get("is_submitter", False)).lower(),
                    "row_type": "comment",
                })

                # Convert None values to empty strings
                for key in comment_row:
                    if comment_row[key] is None:
                        comment_row[key] = ""

                writer.writerow(comment_row)

    return output.getvalue()
