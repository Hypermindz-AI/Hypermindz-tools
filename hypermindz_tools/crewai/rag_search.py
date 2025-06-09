"""
Hypermindz RAG Search Tool for CrewAI
=====================================

This module provides a semantic similarity search tool designed for Retrieval-Augmented 
Generation (RAG) systems within CrewAI workflows.
"""

import os
import requests
from typing import Optional, Dict, Any
from crewai.tools import tool


class HypermindzRAGSearchTool:
    """
    A class to encapsulate the Hypermindz RAG Search functionality.
    
    This tool performs semantic similarity searches over vectorized dataset collections
    to retrieve contextually relevant entries based on user queries.
    """
    
    def __init__(self, api_url: Optional[str] = None, api_key: Optional[str] = None):
        """
        Initialize the RAG Search Tool.
        
        Args:
            api_url (Optional[str]): The API URL. If None, reads from HYPERMINDZ_RAG_URL env var.
            api_key (Optional[str]): The API key. If None, reads from HYPERMINDZ_RAG_API_KEY env var.
        """
        self.api_url = api_url or os.getenv("HYPERMINDZ_RAG_URL")
        self.api_key = api_key or os.getenv("HYPERMINDZ_RAG_API_KEY")
    
    def validate_config(self) -> tuple[bool, str]:
        """
        Validate the configuration.
        
        Returns:
            tuple[bool, str]: (is_valid, error_message)
        """
        if not self.api_url:
            return False, "Error: HYPERMINDZ_RAG_URL not provided or environment variable not set"
        if not self.api_key:
            return False, "Error: HYPERMINDZ_RAG_API_KEY not provided or environment variable not set"
        return True, ""
    
    def search(self, query_text: str, timeout: int = 30) -> str:
        """
        Perform a semantic similarity search.
        
        Args:
            query_text (str): The search query in natural language.
            timeout (int): Request timeout in seconds. Default is 30.
            
        Returns:
            str: Search results or error message.
        """
        # Validate configuration
        is_valid, error_msg = self.validate_config()
        if not is_valid:
            return error_msg
        
        try:
            params = {"query": query_text}
            headers = {"Authorization": f"Bearer {self.api_key}"}
            
            response = requests.get(
                self.api_url, 
                params=params, 
                headers=headers, 
                timeout=timeout
            )
            response.raise_for_status()
            
            # Parse and return results
            results = response.json().get("results", [])
            if not results:
                return "No relevant datasets found."
            
            return str(results)
            
        except requests.exceptions.RequestException as e:
            return f"API request error: {str(e)}"
        except Exception as e:
            return f"Unexpected error: {str(e)}"


# CrewAI tool decorator version
@tool("Hypermindz RAG Search Tool")
def hypermindz_rag_search(query_text: str) -> str:
    """
    Performs a semantic similarity search over a vectorized dataset collection to retrieve the most 
    contextually relevant entries based on the user's input query.

    This tool is designed for use in Retrieval-Augmented Generation (RAG) systems and depends heavily 
    on well-structured, natural language queries to return high-quality results. It sends the input query 
    to a local or remote API that performs vector similarity matching within a predefined dataset collection.

    Args:
        query_text (str): A clear and descriptive query expressed in natural language.
            For best results, use full-sentence queries that capture specific intent 
            (e.g., "List of climate-related policy documents published in 2023").

    Returns:
        str: A formatted string of the most relevant datasets found, or a message indicating 
        no matches were found.

    Notes:
        - Optimized for semantic search in production RAG workflows.
        - Targets a specific dataset collection identified by `collection_id = "json_test"` or by query params.
        - Results depend on the clarity and specificity of the query provided.

    Example:
        query_text = "Datasets about global energy consumption trends from the past decade"
        result = hypermindz_rag_search(query_text)
    """
    tool_instance = HypermindzRAGSearchTool()
    return tool_instance.search(query_text)


# Export both the class and the decorated function
__all__ = ["HypermindzRAGSearchTool", "hypermindz_rag_search"]