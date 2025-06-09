"""
Unit tests for Hypermindz RAG Search Tool
"""

import os
from unittest.mock import Mock, patch

import pytest

from hypermindz_tools.crewai.rag_search import (
    HypermindzRAGSearchTool,
    hypermindz_rag_search,
)


class TestHypermindzRAGSearchTool:
    """Test cases for HypermindzRAGSearchTool class"""

    def test_init_with_parameters(self):
        """Test initialization with direct parameters"""
        tool = HypermindzRAGSearchTool(
            base_url="https://test.com", api_key="test-key", dataset_id="test-dataset"
        )
        assert tool.base_url == "https://test.com"
        assert tool.api_url == "https://test.com/search"
        assert tool.api_key == "test-key"
        assert tool.dataset_id == "test-dataset"

    @patch.dict(
        os.environ,
        {
            "HYPERMINDZ_BASE_URL": "https://env-test.com",
            "HYPERMINDZ_DATASET_ID": "env-dataset",
            "HYPERMINDZ_RAG_API_KEY": "env-test-key",
        },
    )
    def test_init_with_env_vars(self):
        """Test initialization with environment variables"""
        tool = HypermindzRAGSearchTool()
        assert tool.api_url == "https://env-test.com/search"
        assert tool.api_key == "env-test-key"
        assert tool.dataset_id == "env-dataset"

    def test_validate_config_missing_url(self):
        """Test configuration validation with missing URL"""
        tool = HypermindzRAGSearchTool(api_key="test-key", dataset_id="ds")
        is_valid, error_msg = tool.validate_config()
        assert not is_valid
        assert "HYPERMINDZ_BASE_URL" in error_msg

    def test_validate_config_missing_key(self):
        """Test configuration validation with missing API key"""
        tool = HypermindzRAGSearchTool(base_url="https://test.com", dataset_id="ds")
        is_valid, error_msg = tool.validate_config()
        assert not is_valid
        assert "HYPERMINDZ_RAG_API_KEY" in error_msg

    def test_validate_config_missing_dataset(self):
        """Test configuration validation with missing dataset ID"""
        tool = HypermindzRAGSearchTool(base_url="https://test.com", api_key="test-key")
        is_valid, error_msg = tool.validate_config()
        assert not is_valid
        assert "HYPERMINDZ_DATASET_ID" in error_msg

    def test_validate_config_success(self):
        """Test successful configuration validation"""
        tool = HypermindzRAGSearchTool(
            base_url="https://test.com", api_key="test-key", dataset_id="ds"
        )
        is_valid, error_msg = tool.validate_config()
        assert is_valid
        assert error_msg == ""

    @patch("hypermindz_tools.crewai.rag_search.requests.get")
    def test_search_success(self, mock_get):
        """Test successful search"""
        mock_response = Mock()
        mock_response.json.return_value = {"results": ["result1", "result2", "result3"]}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        tool = HypermindzRAGSearchTool(
            base_url="https://test.com", api_key="test-key", dataset_id="ds"
        )
        result = tool.search("test query")

        assert "result1" in result
        assert "result2" in result
        assert "result3" in result

        mock_get.assert_called_once_with(
            "https://test.com/search",
            params={"query": "test query", "id": "ds"},
            headers={"Authorization": "Bearer test-key"},
            timeout=30,
        )

    @patch("hypermindz_tools.crewai.rag_search.requests.get")
    def test_search_no_results(self, mock_get):
        """Test search with no results"""
        mock_response = Mock()
        mock_response.json.return_value = {"results": []}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        tool = HypermindzRAGSearchTool(
            base_url="https://test.com", api_key="test-key", dataset_id="ds"
        )
        result = tool.search("test query")

        assert result == "No relevant datasets found."

    @patch("hypermindz_tools.crewai.rag_search.requests.get")
    def test_search_request_exception(self, mock_get):
        """Test search with request exception"""
        import requests

        mock_get.side_effect = requests.exceptions.RequestException("Connection error")

        tool = HypermindzRAGSearchTool(
            base_url="https://test.com", api_key="test-key", dataset_id="ds"
        )
        result = tool.search("test query")

        assert "API request error" in result
        assert "Connection error" in result

    @patch("hypermindz_tools.crewai.rag_search.requests.get")
    def test_search_general_exception(self, mock_get):
        """Test search with general exception"""
        mock_get.side_effect = Exception("Unexpected error")

        tool = HypermindzRAGSearchTool(
            base_url="https://test.com", api_key="test-key", dataset_id="ds"
        )
        result = tool.search("test query")

        assert "Unexpected error" in result

    def test_search_invalid_config(self):
        """Test search with invalid configuration"""
        tool = HypermindzRAGSearchTool()  # No values
        result = tool.search("test query")

        assert "Error:" in result
        assert "not provided or environment variable not set" in result


class TestHypermindzRAGSearchFunction:
    """Test cases for the decorated function"""

    @patch("hypermindz_tools.crewai.rag_search.HypermindzRAGSearchTool")
    def test_function_calls_tool(self, mock_tool_class):
        """Test that the decorated function creates and uses the tool"""
        # Mock the tool instance
        mock_tool_instance = Mock()
        mock_tool_instance.search.return_value = "test result"
        mock_tool_class.return_value = mock_tool_instance

        # Call the underlying function of the tool
        result = hypermindz_rag_search.func("test query")

        # Verify tool was created and search was called
        mock_tool_class.assert_called_once()
        mock_tool_instance.search.assert_called_once_with("test query")
        assert result == "test result"


if __name__ == "__main__":
    pytest.main([__file__])
