"""
Unit tests for RedditService
"""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from aiohttp import ClientResponse
from src.services.reddit_service import RedditService


class TestRedditService:
    """Tests for RedditService class"""
    
    @pytest.fixture
    def reddit_service(self):
        """Create a RedditService instance for testing"""
        return RedditService()
    
    def test_init(self, reddit_service):
        """Test RedditService initialization"""
        assert reddit_service.base_url == "https://www.reddit.com"
        assert "User-Agent" in reddit_service.headers
    
    def test_build_subreddit_url(self, reddit_service):
        """Test subreddit URL building"""
        url = reddit_service._build_subreddit_url("python", "new", "day", 25)
        assert "r/python/new.json" in url
        assert "limit=25" in url
        
        url = reddit_service._build_subreddit_url("python", "top", "week", 50)
        assert "r/python/top.json" in url
        assert "limit=50" in url
        assert "t=week" in url
    
    def test_build_search_url(self, reddit_service):
        """Test search URL building"""
        url = reddit_service._build_search_url("python tutorial", "new", 25)
        assert "/search.json" in url
        assert "q=python tutorial" in url or "q=python+tutorial" in url or "q=python%20tutorial" in url
        assert "limit=25" in url
        assert "sort=new" in url
    
    @pytest.mark.asyncio
    async def test_get_posts_from_subreddit_success(self, reddit_service):
        """Test successful post fetching"""
        mock_response_data = {
            "data": {
                "children": [
                    {
                        "data": {
                            "id": "test123",
                            "title": "Test Post",
                            "author": "testuser",
                            "subreddit": "python",
                            "score": 100,
                            "created_utc": 1609459200,
                        }
                    }
                ]
            }
        }
        
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value=mock_response_data)
        
        # Make get() return an async context manager
        mock_get_context = AsyncMock()
        mock_get_context.__aenter__ = AsyncMock(return_value=mock_response)
        mock_get_context.__aexit__ = AsyncMock(return_value=None)
        
        mock_session = AsyncMock()
        mock_session.get = MagicMock(return_value=mock_get_context)
        mock_session.__aenter__ = AsyncMock(return_value=mock_session)
        mock_session.__aexit__ = AsyncMock(return_value=None)
        
        with patch("aiohttp.ClientSession", return_value=mock_session):
            posts = await reddit_service.get_posts_from_subreddit("python", "new", "day", 25)
        
        assert len(posts) == 1
        assert posts[0]["id"] == "test123"
        assert posts[0]["title"] == "Test Post"
    
    @pytest.mark.asyncio
    async def test_get_posts_from_subreddit_error(self, reddit_service):
        """Test error handling in post fetching"""
        mock_response = AsyncMock()
        mock_response.status = 404
        
        # Make get() return an async context manager
        mock_get_context = AsyncMock()
        mock_get_context.__aenter__ = AsyncMock(return_value=mock_response)
        mock_get_context.__aexit__ = AsyncMock(return_value=None)
        
        mock_session = AsyncMock()
        mock_session.get = MagicMock(return_value=mock_get_context)
        mock_session.__aenter__ = AsyncMock(return_value=mock_session)
        mock_session.__aexit__ = AsyncMock(return_value=None)
        
        with patch("aiohttp.ClientSession", return_value=mock_session):
            posts = await reddit_service.get_posts_from_subreddit("invalid_subreddit", "new", "day", 25)
        
        assert posts == []
    
    @pytest.mark.asyncio
    async def test_search_posts_success(self, reddit_service):
        """Test successful search"""
        mock_response_data = {
            "data": {
                "children": [
                    {
                        "data": {
                            "id": "search123",
                            "title": "Search Result",
                            "author": "user",
                            "subreddit": "python",
                            "score": 50,
                            "created_utc": 1609459200,
                        }
                    }
                ]
            }
        }
        
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value=mock_response_data)
        
        # Make get() return an async context manager
        mock_get_context = AsyncMock()
        mock_get_context.__aenter__ = AsyncMock(return_value=mock_response)
        mock_get_context.__aexit__ = AsyncMock(return_value=None)
        
        mock_session = AsyncMock()
        mock_session.get = MagicMock(return_value=mock_get_context)
        mock_session.__aenter__ = AsyncMock(return_value=mock_session)
        mock_session.__aexit__ = AsyncMock(return_value=None)
        
        with patch("aiohttp.ClientSession", return_value=mock_session):
            posts = await reddit_service.search_posts("python tutorial", "new", 25)
        
        assert len(posts) == 1
        assert posts[0]["id"] == "search123"
    
    @pytest.mark.asyncio
    async def test_get_comments_for_post_success(self, reddit_service):
        """Test successful comment fetching"""
        mock_response_data = [
            {},  # Post data (not used)
            {
                "data": {
                    "children": [
                        {
                            "kind": "t1",
                            "data": {
                                "id": "comment123",
                                "author": "commenter",
                                "body": "Great post!",
                                "score": 10,
                                "created_utc": 1609459200,
                                "permalink": "/r/test/comments/abc123/",
                            }
                        }
                    ]
                }
            }
        ]
        
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value=mock_response_data)
        
        # Make get() return an async context manager
        mock_get_context = AsyncMock()
        mock_get_context.__aenter__ = AsyncMock(return_value=mock_response)
        mock_get_context.__aexit__ = AsyncMock(return_value=None)
        
        mock_session = AsyncMock()
        mock_session.get = MagicMock(return_value=mock_get_context)
        mock_session.__aenter__ = AsyncMock(return_value=mock_session)
        mock_session.__aexit__ = AsyncMock(return_value=None)
        
        with patch("aiohttp.ClientSession", return_value=mock_session):
            comments = await reddit_service.get_comments_for_post("abc123", "test", 10)
        
        assert len(comments) == 1
        assert comments[0]["id"] == "comment123"
        assert comments[0]["body"] == "Great post!"
    
    @pytest.mark.asyncio
    async def test_get_comments_for_post_empty(self, reddit_service):
        """Test comment fetching with max_comments = 0"""
        comments = await reddit_service.get_comments_for_post("abc123", "test", 0)
        assert comments == []
    
    @pytest.mark.asyncio
    async def test_get_comments_for_post_filters_deleted(self, reddit_service):
        """Test that deleted comments are filtered out"""
        mock_response_data = [
            {},
            {
                "data": {
                    "children": [
                        {
                            "kind": "t1",
                            "data": {
                                "id": "comment123",
                                "author": "commenter",
                                "body": "[deleted]",
                                "score": 10,
                                "created_utc": 1609459200,
                                "permalink": "/r/test/comments/abc123/",
                            }
                        }
                    ]
                }
            }
        ]
        
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value=mock_response_data)
        
        # Make get() return an async context manager
        mock_get_context = AsyncMock()
        mock_get_context.__aenter__ = AsyncMock(return_value=mock_response)
        mock_get_context.__aexit__ = AsyncMock(return_value=None)
        
        mock_session = AsyncMock()
        mock_session.get = MagicMock(return_value=mock_get_context)
        mock_session.__aenter__ = AsyncMock(return_value=mock_session)
        mock_session.__aexit__ = AsyncMock(return_value=None)
        
        with patch("aiohttp.ClientSession", return_value=mock_session):
            comments = await reddit_service.get_comments_for_post("abc123", "test", 10)
        
        # Deleted comments should be filtered out
        assert len(comments) == 0

