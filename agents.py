from crewai import Agent
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key
google_api_key = os.getenv("GOOGLE_API_KEY")

if not google_api_key:
    raise ValueError("GOOGLE_API_KEY not found in .env file!")

# Initialize Gemini LLM with correct model name
llm = ChatGoogleGenerativeAI(
    model="gemini-pro-latest",
    google_api_key=google_api_key,
    temperature=0.7,
    max_tokens=2048
)

# Define Research Agent
research_agent = Agent(
    role='Senior Research Analyst',
    goal='Conduct thorough research on the given topic and gather comprehensive information',
    backstory="""You are an expert research analyst with years of experience and 
    deep knowledge across multiple domains. You can provide detailed, accurate 
    information on a wide range of topics including technology, science, business, 
    health, and more. You draw from your extensive training data to provide 
    current and relevant insights.""",
    verbose=True,
    allow_delegation=False,
    llm=llm,
    max_iter=5,
    max_action_retries=2
)

# Define Analysis Agent
analysis_agent = Agent(
    role='Data Analysis Expert',
    goal='Analyze research findings and identify key insights',
    backstory="""You are a data analysis expert who excels at finding patterns, 
    validating information, and extracting meaningful insights from complex data. 
    You can identify trends, correlations, and strategic implications. Your 
    analysis helps stakeholders make informed decisions.""",
    verbose=True,
    allow_delegation=False,
    llm=llm,
    max_iter=5,
    max_action_retries=2
)

# Define Writer Agent
writer_agent = Agent(
    role='Technical Content Writer',
    goal='Create a comprehensive and professional research report',
    backstory="""You are a skilled technical writer who can transform complex 
    research and analysis into clear, engaging, and well-structured reports. 
    Your reports follow professional formatting standards and include:
    - Executive summaries
    - Clear section headings
    - Key findings and insights
    - Actionable recommendations
    - Professional conclusions""",
    verbose=True,
    allow_delegation=False,
    llm=llm,
    max_iter=5,
    max_action_retries=2
)
