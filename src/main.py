"""
Reddit Scraper Actor - Main Entry Point

Scrapes Reddit posts, comments, and threads from subreddits using Reddit's public API.
No authentication required. Challenge-compliant for Apify $1M Challenge.

Based on TradeX reddit_service.py implementation, adapted for Apify platform.
"""

import asyncio
from datetime import datetime
from typing import List, Dict, Any
from apify import Actor

from src.config import (
    DEFAULT_SORT,
    DEFAULT_TIME_FILTER,
    DEFAULT_LIMIT,
    DEFAULT_MAX_COMMENTS,
    DELAY_BETWEEN_SUBREDDITS_SECONDS,
)
from src.services.reddit_service import RedditService
from src.utils.helpers import validate_input


async def scrape_subreddits(
    reddit_service: RedditService,
    subreddits: List[str],
    sort: str,
    time_filter: str,
    limit: int,
    include_comments: bool,
    max_comments_per_post: int,
) -> List[Dict]:
    """
    Scrape multiple subreddits
    
    Args:
        reddit_service: RedditService instance
        subreddits: List of subreddit names
        sort: Sort order
        time_filter: Time filter for 'top' sort
        limit: Max posts per subreddit
        include_comments: Whether to fetch comments
        max_comments_per_post: Max comments per post
        
    Returns:
        List of all scraped posts
    """
    all_posts = []
    
    Actor.log.info(f"Scraping {len(subreddits)} subreddit(s)")
    
    for i, subreddit in enumerate(subreddits):
        try:
            posts = await reddit_service.get_posts_from_subreddit(
                subreddit=subreddit,
                sort=sort,
                time_filter=time_filter,
                limit=limit,
            )
            
            # Fetch comments if requested
            if include_comments:
                for post in posts:
                    if post.get("num_comments", 0) > 0:
                        comments = await reddit_service.get_comments_for_post(
                            post_id=post["id"],
                            subreddit=post["subreddit"],
                            max_comments=max_comments_per_post,
                        )
                        post["comments"] = comments
            
            all_posts.extend(posts)
            
            # Add delay between subreddits to be respectful
            if i < len(subreddits) - 1:
                await asyncio.sleep(DELAY_BETWEEN_SUBREDDITS_SECONDS)
                
        except Exception as e:
            Actor.log.error(f"Error scraping subreddit {subreddit}: {e}")
            continue
    
    return all_posts


async def search_reddit(
    reddit_service: RedditService,
    query: str,
    sort: str,
    limit: int,
    include_comments: bool,
    max_comments_per_post: int,
) -> List[Dict]:
    """
    Search Reddit for posts
    
    Args:
        reddit_service: RedditService instance
        query: Search query
        sort: Sort order
        limit: Max results
        include_comments: Whether to fetch comments
        max_comments_per_post: Max comments per post
        
    Returns:
        List of search results
    """
    posts = await reddit_service.search_posts(query=query, sort=sort, limit=limit)
    
    # Fetch comments if requested
    if include_comments:
        for post in posts:
            if post.get("num_comments", 0) > 0:
                comments = await reddit_service.get_comments_for_post(
                    post_id=post["id"],
                    subreddit=post["subreddit"],
                    max_comments=max_comments_per_post,
                )
                post["comments"] = comments
    
    return posts


async def run_scraper(input_data: Dict[str, Any]):
    """Run the scraper logic (without Actor context manager)"""
    # This function is called from main.py which manages the Actor context
    # Get input configuration (already passed as parameter)
    
    # Extract and set defaults
    subreddits = input_data.get("subreddits", [])
    search_query = input_data.get("searchQuery", "")
    sort_by = input_data.get("sortBy", DEFAULT_SORT)
    time_filter = input_data.get("timeFilter", DEFAULT_TIME_FILTER)
    limit = input_data.get("limit", DEFAULT_LIMIT)
    include_comments = input_data.get("includeComments", False)
    max_comments_per_post = input_data.get("maxCommentsPerPost", DEFAULT_MAX_COMMENTS)
    
    # Validate input
    try:
        validate_input(input_data)
    except ValueError as e:
        Actor.log.error(f"Input validation failed: {e}")
        await Actor.fail(exit_code=1)
        return
    
    Actor.log.info("Starting Reddit scraper", {
        "subreddits": len(subreddits),
        "searchQuery": search_query or "none",
        "sortBy": sort_by,
        "limit": limit,
        "includeComments": include_comments,
    })
    
    # Initialize Reddit service
    reddit_service = RedditService()
    
    # Scrape data
    all_posts = []
    
    try:
        # Scrape subreddits if provided
        if subreddits:
            posts = await scrape_subreddits(
                reddit_service=reddit_service,
                subreddits=subreddits,
                sort=sort_by,
                time_filter=time_filter,
                limit=limit,
                include_comments=include_comments,
                max_comments_per_post=max_comments_per_post,
            )
            all_posts.extend(posts)
        
        # Search Reddit if query provided
        if search_query:
            search_posts = await search_reddit(
                reddit_service=reddit_service,
                query=search_query,
                sort=sort_by,
                limit=limit,
                include_comments=include_comments,
                max_comments_per_post=max_comments_per_post,
            )
            all_posts.extend(search_posts)
        
        # Save all posts to dataset
        if all_posts:
            Actor.log.info(f"Saving {len(all_posts)} posts to dataset")
            
            for post in all_posts:
                await Actor.push_data(post)
            
            Actor.log.info(f"Successfully scraped and saved {len(all_posts)} Reddit posts")
        else:
            Actor.log.warning("No posts were scraped. Check your input parameters.")
        
        # Set summary statistics
        await Actor.set_value("summary", {
            "totalPosts": len(all_posts),
            "subredditsScraped": len(subreddits),
            "searchQuery": search_query or None,
            "timestamp": datetime.now().isoformat(),
        })
        
    except Exception as e:
        Actor.log.error("Fatal error in Reddit scraper", {
            "error": str(e),
            "type": type(e).__name__,
        })
        await Actor.fail(exit_code=1)

