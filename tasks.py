from crewai import Task
from agents import research_agent, analysis_agent, writer_agent

def create_research_tasks(topic):
    # Task 1: Research
    research_task = Task(
        description=f"""Conduct comprehensive research on {topic}.
        
        Your tasks:
        1. Search for the latest information and developments
        2. Identify key facts, statistics, and expert opinions
        3. Gather information from multiple perspectives
        4. Note important sources and references
        
        Provide a detailed research summary with all findings.""",
        agent=research_agent,
        expected_output="Detailed research summary with key findings and sources"
    )
    
    # Task 2: Analysis
    analysis_task = Task(
        description=f"""Analyze the research findings on {topic}.
        
        Your tasks:
        1. Identify key themes and patterns
        2. Validate the credibility of information
        3. Extract the most important insights
        4. Highlight any contradictions or debates
        5. Provide strategic recommendations
        
        Create a structured analysis report.""",
        agent=analysis_agent,
        expected_output="Comprehensive analysis with insights and recommendations",
        context=[research_task]
    )
    
    # Task 3: Writing
    writing_task = Task(
        description=f"""Create a comprehensive research report on {topic}.
        
        Your report should include:
        1. Executive Summary (2-3 paragraphs)
        2. Introduction
        3. Key Findings (organized by themes)
        4. Detailed Analysis
        5. Conclusions and Recommendations
        6. References
        
        Make it professional, clear, and engaging.""",
        agent=writer_agent,
        expected_output="Professional research report in markdown format",
        context=[research_task, analysis_task]
    )
    
    return [research_task, analysis_task, writing_task]
