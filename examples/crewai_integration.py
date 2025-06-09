"""
CrewAI integration example for Hypermindz RAG Search Tool
"""

from crewai import Agent, Task, Crew
from hypermindz_tools.crewai import hypermindz_rag_search

def main():
    print("=== Hypermindz RAG Search Tool - CrewAI Integration ===\n")
    
    # Create a research agent with the RAG search tool
    researcher = Agent(
        role='Senior Research Analyst',
        goal='Find and analyze relevant datasets and research materials',
        backstory="""You are a seasoned research analyst with expertise in data discovery 
                    and analysis. You excel at finding relevant information from large 
                    collections of datasets and can quickly identify the most pertinent 
                    sources for any given research question.""",
        tools=[hypermindz_rag_search],
        verbose=True,
        allow_delegation=False
    )
    
    # Create a data analyst agent
    analyst = Agent(
        role='Data Quality Analyst',
        goal='Evaluate and summarize the quality and relevance of found datasets',
        backstory="""You are an expert in data quality assessment and can quickly 
                    evaluate the relevance, completeness, and reliability of datasets. 
                    You provide clear summaries and recommendations.""",
        verbose=True,
        allow_delegation=False
    )
    
    # Create research tasks
    research_task = Task(
        description="""Find datasets related to renewable energy adoption trends, 
                      specifically focusing on solar and wind energy implementation 
                      in developing countries over the past 5 years.""",
        agent=researcher,
        expected_output="""A comprehensive list of relevant datasets with descriptions, 
                          sources, and brief summaries of their content and scope."""
    )
    
    analysis_task = Task(
        description="""Based on the datasets found by the researcher, provide an analysis 
                      of their quality, relevance, and potential usefulness for studying 
                      renewable energy trends in developing countries.""",
        agent=analyst,
        expected_output="""A detailed analysis report ranking the datasets by quality 
                          and relevance, with recommendations for the most valuable 
                          sources for further research."""
    )
    
    # Create and configure the crew
    crew = Crew(
        agents=[researcher, analyst],
        tasks=[research_task, analysis_task],
        verbose=2,
        process=None  # Sequential process
    )
    
    try:
        print("Starting CrewAI workflow with Hypermindz RAG Search Tool...\n")
        result = crew.kickoff()
        
        print("\n=== FINAL RESULTS ===")
        print(result)
        
    except Exception as e:
        print(f"Error during CrewAI execution: {e}")

def simple_agent_example():
    """A simpler example with just one agent"""
    
    print("\n=== Simple Agent Example ===\n")
    
    # Create a simple research agent
    researcher = Agent(
        role='Data Researcher',
        goal='Find relevant datasets using semantic search',
        backstory='You are skilled at finding relevant data sources.',
        tools=[hypermindz_rag_search],
        verbose=True
    )
    
    # Create a simple task
    task = Task(
        description='Find datasets about climate change impacts on agriculture',
        agent=researcher,
        expected_output='List of relevant datasets with brief descriptions'
    )
    
    # Create crew with single agent
    crew = Crew(
        agents=[researcher],
        tasks=[task],
        verbose=1
    )
    
    try:
        result = crew.kickoff()
        print(f"\nSimple example result:\n{result}")
    except Exception as e:
        print(f"Error in simple example: {e}")

if __name__ == "__main__":
    # Make sure to set your environment variables first:
    # export HYPERMINDZ_RAG_URL="https://your-api-endpoint.com"
    # export HYPERMINDZ_RAG_API_KEY="your-api-key"
    
    # Run the complex example
    main()
    
    # Run the simple example
    simple_agent_example()