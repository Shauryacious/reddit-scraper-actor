"""
Reddit Service
Handles all Reddit API interactions for scraping posts and comments
Uses Reddit's public API (no authentication required)
"""

from typing import Dict, List, Optional

import aiohttp
from apify import Actor

from src.config import (DELAY_BETWEEN_SUBREDDITS_SECONDS,
                        MAX_COMMENTS_PER_REQUEST, MAX_POSTS_PER_REQUEST,
                        REDDIT_BASE_URL, REDDIT_USER_AGENT, VALID_SORT_OPTIONS,
                        VALID_TIME_FILTERS)
from src.utils.helpers import (clean_subreddit_name, normalize_comment_data,
                               normalize_post_data)


class RedditService:
    """Service for Reddit API interactions (free, no auth required)"""

    def __init__(self):
        """Initialize Reddit service"""
        self.base_url = REDDIT_BASE_URL
        self.headers = {"User-Agent": REDDIT_USER_AGENT}
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

            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=self.headers) as response:
                    if response.status == 200:
                        data = await response.json()
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
                        Actor.log.warning(
                            f"Reddit API returned status {response.status} for r/{clean_name}"
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

            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=self.headers) as response:
                    if response.status == 200:
                        data = await response.json()
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
                        Actor.log.warning(
                            f"Reddit search API returned status {response.status}"
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

            async with aiohttp.ClientSession() as session:
                async with session.get(full_url, headers=self.headers) as response:
                    if response.status == 200:
                        data = await response.json()
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
                        Actor.log.warning(
                            f"Failed to fetch comments for post {post_id}: "
                            f"status {response.status}"
                        )
                        return []
        except Exception as e:
            Actor.log.error(f"Error fetching comments for post {post_id}: {e}")
            return []
