# Hypermindz Tools

A collection of tools by the Hypermindz for AI workflows, including CrewAI integrations.

## Installation

```bash
pip install hypermindz-tools
```

## Features

- **CrewAI Integration**: Tools specifically designed for CrewAI workflows
- **RAG Search**: Semantic similarity search over vectorized datasets
- **Easy Configuration**: Environment variable or direct parameter configuration

## Quick Start

### Using the CrewAI Tool

```python
from hypermindz_tools.crewai import hypermindz_rag_search

# Set environment variables
# HYPERMINDZ_BASE_URL=https://api.hypermindz.com
# HYPERMINDZ_DATASET_ID=your_dataset_id
# HYPERMINDZ_RAG_API_KEY=your_api_key

# Use the tool
result = hypermindz_rag_search("Find datasets about climate change")
print(result)
```

### Integration with CrewAI Agents

```python
from crewai import Agent, Task, Crew
from hypermindz_tools.crewai import hypermindz_rag_search

# Create an agent with the RAG search tool
researcher = Agent(
    role='Research Analyst',
    goal='Find and analyze relevant datasets',
    backstory='You are an expert at finding relevant information from large datasets.',
    tools=[hypermindz_rag_search],
    verbose=True
)

# Create a task
research_task = Task(
    description='Find datasets related to sustainable energy practices',
    agent=researcher,
    expected_output='A list of relevant datasets with descriptions'
)

# Create and run crew
crew = Crew(
    agents=[researcher],
    tasks=[research_task],
    verbose=2
)

result = crew.kickoff()
```

## Configuration

### Environment Variables

Set the following environment variables:

```bash
export HYPERMINDZ_BASE_URL="https://api.hypermindz.com"
export HYPERMINDZ_DATASET_ID="your_dataset_id"
export HYPERMINDZ_RAG_API_KEY="your_api_key"
```

## API Reference

### HypermindzRAGSearchTool

#### Methods

- `__init__(base_url=None, dataset_id=None, api_key=None)`: Initialize the tool
- `search(query_text, timeout=30)`: Perform semantic search
- `validate_config()`: Validate configuration

#### Parameters

- `base_url (str)`: Base URL of the Hypermindz API
- `dataset_id (str)`: Dataset ID to search within (sent as 'id' parameter)
- `api_key (str)`: API key for authentication
- `query_text (str)`: Natural language query for semantic search
- `timeout (int)`: Request timeout in seconds (default: 30)

### hypermindz_rag_search

Decorated function for direct use with CrewAI.

#### Parameters

- `query_text (str)`: Natural language query for semantic search

#### Returns

- `str`: Search results or error message

## Examples

### Basic Usage

```python
from hypermindz_tools.crewai import hypermindz_rag_search

# Simple search
result = hypermindz_rag_search("Datasets about global warming trends")
```

## Request Format

The tool makes requests in the following format:
```
GET {base_url}/search?query={your_query}&id={dataset_id}
Authorization: Bearer {api_key}
```

Example:
```
GET https://api.hypermindz.com/search?query=renewable+energy+datasets&id=energy_data_2023
Authorization: Bearer your_api_key_here
```

## Requirements

- Python >= 3.8
- requests >= 2.25.0
- crewai >= 0.1.0

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/Hypermindz-AI/Hypermindz-tools.git
cd hypermindz-tools

# Install in development mode
pip install -e .[dev]
```

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
black hypermindz_tools/
flake8 hypermindz_tools/
```

## License

MIT License

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Support

For issues and questions, please open an issue on GitHub.