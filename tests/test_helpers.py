"""
Unit tests for helper utility functions
"""

import pytest
from datetime import datetime, timezone
from src.utils.helpers import (
    clean_subreddit_name,
    format_timestamp,
    validate_input,
    normalize_post_data,
    normalize_comment_data,
)


class TestCleanSubredditName:
    """Tests for clean_subreddit_name function"""
    
    def test_removes_r_prefix(self):
        assert clean_subreddit_name("r/python") == "python"
        assert clean_subreddit_name("r/learnpython") == "learnpython"
    
    def test_keeps_name_without_prefix(self):
        assert clean_subreddit_name("python") == "python"
        assert clean_subreddit_name("learnpython") == "learnpython"
    
    def test_handles_whitespace(self):
        assert clean_subreddit_name("  r/python  ") == "python"
        assert clean_subreddit_name("  python  ") == "python"
    
    def test_handles_multiple_r_prefixes(self):
        # The function strips all "r/" prefixes, so "rr/python" becomes "python"
        assert clean_subreddit_name("rr/python") == "python"


class TestFormatTimestamp:
    """Tests for format_timestamp function"""
    
    def test_formats_timestamp_correctly(self):
        timestamp = 1609459200  # 2021-01-01 00:00:00 UTC
        result = format_timestamp(timestamp)
        assert isinstance(result, str)
        assert "2021-01-01" in result
        assert "T" in result  # ISO format includes T
    
    def test_handles_zero_timestamp(self):
        result = format_timestamp(0)
        assert isinstance(result, str)
        assert "1970-01-01" in result


class TestValidateInput:
    """Tests for validate_input function"""
    
    def test_validates_with_subreddits(self):
        input_data = {"subreddits": ["python", "javascript"]}
        # Should not raise
        validate_input(input_data)
    
    def test_validates_with_search_query(self):
        input_data = {"searchQuery": "python tutorial"}
        # Should not raise
        validate_input(input_data)
    
    def test_raises_error_when_both_empty(self):
        input_data = {}
        with pytest.raises(ValueError, match="Either 'subreddits' or 'searchQuery' must be provided"):
            validate_input(input_data)
    
    def test_raises_error_for_invalid_sort(self):
        input_data = {"subreddits": ["python"], "sortBy": "invalid"}
        with pytest.raises(ValueError, match="Invalid sortBy"):
            validate_input(input_data)
    
    def test_validates_valid_sort_options(self):
        for sort in ["new", "hot", "top", "rising"]:
            input_data = {"subreddits": ["python"], "sortBy": sort}
            validate_input(input_data)  # Should not raise
    
    def test_raises_error_for_invalid_limit(self):
        input_data = {"subreddits": ["python"], "limit": 0}
        with pytest.raises(ValueError, match="limit must be an integer between 1 and 100"):
            validate_input(input_data)
        
        input_data = {"subreddits": ["python"], "limit": 101}
        with pytest.raises(ValueError, match="limit must be an integer between 1 and 100"):
            validate_input(input_data)
        
        input_data = {"subreddits": ["python"], "limit": "25"}
        with pytest.raises(ValueError, match="limit must be an integer between 1 and 100"):
            validate_input(input_data)
    
    def test_validates_valid_limit(self):
        for limit in [1, 25, 50, 100]:
            input_data = {"subreddits": ["python"], "limit": limit}
            validate_input(input_data)  # Should not raise


class TestNormalizePostData:
    """Tests for normalize_post_data function"""
    
    def test_normalizes_post_data_correctly(self):
        post_data = {
            "id": "abc123",
            "title": "Test Post",
            "selftext": "Test content",
            "author": "testuser",
            "subreddit": "test",
            "score": 100,
            "upvote_ratio": 0.95,
            "num_comments": 50,
            "created_utc": 1609459200,
            "url": "https://example.com",
            "permalink": "/r/test/comments/abc123/test_post/",
            "is_self": True,
            "is_video": False,
            "thumbnail": "https://example.com/thumb.jpg",
            "domain": "self.test",
        }
        
        result = normalize_post_data(post_data, "subreddit", "test")
        
        assert result["id"] == "abc123"
        assert result["title"] == "Test Post"
        assert result["author"] == "testuser"
        assert result["subreddit"] == "test"
        assert result["score"] == 100
        assert result["source_type"] == "subreddit"
        assert result["source_name"] == "test"
        assert "reddit.com" in result["permalink"]
        assert isinstance(result["created_at"], str)
    
    def test_handles_missing_fields(self):
        post_data = {}
        result = normalize_post_data(post_data, "search", "query")
        
        assert result["id"] == ""
        assert result["title"] == ""
        assert result["author"] == "[deleted]"
        assert result["score"] == 0
        assert result["source_type"] == "search"
        assert result["source_name"] == "query"


class TestNormalizeCommentData:
    """Tests for normalize_comment_data function"""
    
    def test_normalizes_comment_data_correctly(self):
        comment_data = {
            "id": "def456",
            "author": "commenter",
            "body": "Great post!",
            "score": 25,
            "created_utc": 1609459200,
            "permalink": "/r/test/comments/abc123/test_post/def456/",
            "is_submitter": False,
            "parent_id": "t3_abc123",
        }
        
        result = normalize_comment_data(comment_data, "abc123")
        
        assert result["id"] == "def456"
        assert result["author"] == "commenter"
        assert result["body"] == "Great post!"
        assert result["score"] == 25
        assert result["post_id"] == "abc123"
        assert "reddit.com" in result["permalink"]
        assert isinstance(result["created_at"], str)
    
    def test_handles_missing_fields(self):
        comment_data = {}
        result = normalize_comment_data(comment_data, "abc123")
        
        assert result["id"] == ""
        assert result["author"] == "[deleted]"
        assert result["body"] == ""
        assert result["score"] == 0
        assert result["post_id"] == "abc123"

