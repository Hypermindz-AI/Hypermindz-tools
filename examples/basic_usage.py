"""
Basic usage example for Hypermindz RAG Search Tool
"""

from hypermindz_tools.crewai import HypermindzRAGSearchTool, hypermindz_rag_search


def main():
    print("=== Hypermindz RAG Search Tool - Basic Usage ===\n")

    # Method 1: Using the decorated function
    print("1. Using the decorated function:")
    try:
        result = hypermindz_rag_search("Find datasets about climate change and global warming")
        print(f"Result: {result}\n")
    except Exception as e:
        print(f"Error: {e}\n")

    # Method 2: Using the class
    print("2. Using the tool class:")
    try:
        # Initialize with environment variables
        tool = HypermindzRAGSearchTool()

        # Validate configuration
        is_valid, error_msg = tool.validate_config()
        if not is_valid:
            print(f"Configuration error: {error_msg}")
            return

        # Perform search
        result = tool.search("Datasets about renewable energy and sustainability")
        print(f"Result: {result}\n")

    except Exception as e:
        print(f"Error: {e}\n")

    # Method 3: Using the class with direct parameters
    print("3. Using the tool class with direct parameters:")
    try:
        # You would replace these with your actual API details
        tool = HypermindzRAGSearchTool(api_url="https://your-api-endpoint.com", api_key="your-api-key")

        result = tool.search("Find research papers on artificial intelligence")
        print(f"Result: {result}\n")

    except Exception as e:
        print(f"Error: {e}\n")


if __name__ == "__main__":
    # Make sure to set your environment variables first:
    # export HYPERMINDZ_RAG_URL="https://your-api-endpoint.com"
    # export HYPERMINDZ_RAG_API_KEY="your-api-key"

    main()
