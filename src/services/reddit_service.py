"""
Reddit Service
Handles all Reddit API interactions for scraping posts and comments
Uses Reddit's public API (no authentication required)
"""

import asyncio
from typing import Dict, List, Optional, Tuple

import aiohttp
from apify import Actor

from src.config import (
    DELAY_BETWEEN_SUBREDDITS_SECONDS,
    MAX_COMMENTS_PER_REQUEST,
    MAX_POSTS_PER_REQUEST,
    REDDIT_BASE_URL,
    REDDIT_USER_AGENT,
    VALID_SORT_OPTIONS,
    VALID_TIME_FILTERS,
)
from src.utils.helpers import (
    clean_subreddit_name,
    normalize_comment_data,
    normalize_post_data,
)


class RedditService:
    """Service for Reddit API interactions (free, no auth required)"""

    def __init__(self):
        """Initialize Reddit service"""
        self.base_url = REDDIT_BASE_URL
        # Use browser-like headers to avoid 403 errors from Reddit
        self.headers = {
            "User-Agent": REDDIT_USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        }
        Actor.log.info("Reddit service initialized (free, no authentication required)")

    def _build_subreddit_url(
        self,
        subreddit: str,
        sort: str = "new",
        time_filter: str = "day",
        limit: int = 25,
    ) -> str:
        """
        Build Reddit API URL for subreddit posts

        Args:
            subreddit: Subreddit name (will be cleaned)
            sort: Sort order (new, hot, top, rising)
            time_filter: Time filter for 'top' sort
            limit: Number of posts to fetch

        Returns:
            Complete Reddit API URL
        """
        clean_name = clean_subreddit_name(subreddit)
        url = f"{self.base_url}/r/{clean_name}/{sort}.json"
        params = {"limit": str(min(limit, MAX_POSTS_PER_REQUEST))}

        if sort == "top" and time_filter in VALID_TIME_FILTERS:
            params["t"] = time_filter

        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        return f"{url}?{query_string}"

    def _build_search_url(self, query: str, sort: str = "new", limit: int = 25) -> str:
        """
        Build Reddit search API URL

        Args:
            query: Search query
            sort: Sort order
            limit: Number of results

        Returns:
            Complete Reddit search API URL
        """
        url = f"{self.base_url}/search.json"
        params = {
            "q": query,
            "limit": str(min(limit, MAX_POSTS_PER_REQUEST)),
            "sort": sort,
        }
        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        return f"{url}?{query_string}"

    async def _make_request_with_retry(
        self, url: str, max_retries: int = 3, retry_delay: float = 2.0
    ) -> Tuple[Optional[int], Optional[Dict]]:
        """
        Make HTTP request with retry logic for 403 errors

        Args:
            url: URL to request
            max_retries: Maximum number of retries
            retry_delay: Initial delay between retries (exponential backoff)

        Returns:
            Tuple of (status_code, response_data) or (None, None) if all retries failed
        """
        for attempt in range(max_retries):
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url, headers=self.headers) as response:
                        if response.status == 200:
                            try:
                                data = await response.json()
                                return (response.status, data)
                            except Exception as e:
                                Actor.log.error(f"Failed to parse JSON response: {e}")
                                return (response.status, None)
                        elif response.status == 403 and attempt < max_retries - 1:
                            # Wait before retrying with exponential backoff
                            wait_time = retry_delay * (2 ** attempt)
                            Actor.log.warning(
                                f"Got 403 error, retrying in {wait_time}s (attempt {attempt + 1}/{max_retries})"
                            )
                            await asyncio.sleep(wait_time)
                            continue
                        else:
                            # For non-200, non-403 statuses, try to read error text
                            try:
                                error_text = await response.text()
                                return (response.status, {"error": error_text})
                            except Exception:
                                return (response.status, None)
            except Exception as e:
                if attempt < max_retries - 1:
                    wait_time = retry_delay * (2 ** attempt)
                    Actor.log.warning(
                        f"Request failed, retrying in {wait_time}s (attempt {attempt + 1}/{max_retries}): {e}"
                    )
                    await asyncio.sleep(wait_time)
                else:
                    Actor.log.error(f"Request failed after {max_retries} attempts: {e}")
        return (None, None)

    async def get_posts_from_subreddit(
        self,
        subreddit: str,
        sort: str = "new",
        time_filter: str = "day",
        limit: int = 25,
    ) -> List[Dict]:
        """
        Get posts from a subreddit

        Args:
            subreddit: Subreddit name (with or without r/ prefix)
            sort: Sort order (new, hot, top, rising)
            time_filter: Time filter for 'top' sort
            limit: Number of posts to fetch (max 100)

        Returns:
            List of post dictionaries
        """
        try:
            clean_name = clean_subreddit_name(subreddit)
            url = self._build_subreddit_url(clean_name, sort, time_filter, limit)

            Actor.log.debug(f"Fetching posts from r/{clean_name}", {"url": url})

            status_code, data = await self._make_request_with_retry(url)
            if status_code is None or data is None:
                Actor.log.error(f"Failed to fetch posts from r/{clean_name} after retries")
                return []

            if status_code == 200:
                posts = []

                if "data" in data and "children" in data["data"]:
                    for child in data["data"]["children"]:
                        post_data = child.get("data", {})
                        normalized_post = normalize_post_data(
                            post_data, "subreddit", clean_name
                        )
                        posts.append(normalized_post)

                Actor.log.info(
                    f"Fetched {len(posts)} posts from r/{clean_name}"
                )
                return posts
            else:
                # Log response body for debugging 403 errors
                error_text = data.get("error", "") if isinstance(data, dict) else str(data)
                Actor.log.warning(
                    f"Reddit API returned status {status_code} for r/{clean_name}",
                    {"response_preview": error_text[:200] if error_text else "No response body"}
                )
                return []
        except Exception as e:
            Actor.log.error(f"Error fetching posts from r/{subreddit}: {e}")
            return []

    async def search_posts(
        self, query: str, sort: str = "new", limit: int = 25
    ) -> List[Dict]:
        """
        Search Reddit for posts matching a query

        Args:
            query: Search query
            sort: Sort order
            limit: Number of results

        Returns:
            List of post dictionaries
        """
        try:
            url = self._build_search_url(query, sort, limit)

            Actor.log.debug(f"Searching Reddit for: '{query}'", {"url": url})

            status_code, data = await self._make_request_with_retry(url)
            if status_code is None or data is None:
                Actor.log.error(f"Failed to search Reddit after retries")
                return []

            if status_code == 200:
                posts = []

                if "data" in data and "children" in data["data"]:
                    for child in data["data"]["children"]:
                        post_data = child.get("data", {})
                        normalized_post = normalize_post_data(
                            post_data, "search", query
                        )
                        posts.append(normalized_post)

                Actor.log.info(
                    f"Found {len(posts)} posts for search query: '{query}'"
                )
                return posts
            else:
                # Log response body for debugging
                error_text = data.get("error", "") if isinstance(data, dict) else str(data)
                Actor.log.warning(
                    f"Reddit search API returned status {status_code}",
                    {"response_preview": error_text[:200] if error_text else "No response body"}
                )
                return []
        except Exception as e:
            Actor.log.error(f"Error searching Reddit: {e}")
            return []

    async def get_comments_for_post(
        self, post_id: str, subreddit: str, max_comments: int = 10
    ) -> List[Dict]:
        """
        Fetch comments for a specific post

        Args:
            post_id: Reddit post ID
            subreddit: Subreddit name
            max_comments: Maximum number of comments to fetch

        Returns:
            List of comment dictionaries
        """
        if max_comments <= 0:
            return []

        try:
            clean_name = clean_subreddit_name(subreddit)
            url = f"{self.base_url}/r/{clean_name}/comments/{post_id}.json"
            params = {"limit": str(min(max_comments, MAX_COMMENTS_PER_REQUEST))}
            query_string = "&".join([f"{k}={v}" for k, v in params.items()])
            full_url = f"{url}?{query_string}"

            Actor.log.debug(
                f"Fetching comments for post {post_id}",
                {"subreddit": clean_name, "max_comments": max_comments},
            )

            status_code, data = await self._make_request_with_retry(full_url)
            if status_code is None or data is None:
                Actor.log.error(f"Failed to fetch comments for post {post_id} after retries")
                return []

            if status_code == 200:
                comments = []

                # Reddit comments API returns array: [post data, comments data]
                if isinstance(data, list) and len(data) > 1:
                    comments_data = data[1].get("data", {}).get("children", [])

                    for child in comments_data[:max_comments]:
                        comment_data = child.get("data", {})

                        # Skip "more" objects and deleted comments
                        if (
                            child.get("kind") == "t1"
                            and comment_data.get("body")
                            and comment_data.get("body") != "[deleted]"
                        ):
                            normalized_comment = normalize_comment_data(
                                comment_data, post_id
                            )
                            comments.append(normalized_comment)

                Actor.log.debug(
                    f"Fetched {len(comments)} comments for post {post_id}"
                )
                return comments
            else:
                # Log response body for debugging
                error_text = data.get("error", "") if isinstance(data, dict) else str(data)
                Actor.log.warning(
                    f"Failed to fetch comments for post {post_id}: "
                    f"status {status_code}",
                    {"response_preview": error_text[:200] if error_text else "No response body"}
                )
                return []
        except Exception as e:
            Actor.log.error(f"Error fetching comments for post {post_id}: {e}")
            return []
