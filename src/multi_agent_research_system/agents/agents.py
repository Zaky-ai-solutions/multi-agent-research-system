from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
#from langchain_core.output_parsers import StructuredOutputParser
from langchain_core.prompts import ChatPromptTemplate
from src.multi_agent_research_system.tools.tools import web_search, scrape_url  
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file
# model initialization
llm = ChatOpenAI(model = "openai/gpt-oss-20b", temperature=0.2, max_tokens=2000)  # Initialize the language model

# will search internet and get urls
def build_search_agent():
    return create_agent(
        model = llm,
        tools = [web_search],     
    )

# will extract the content of the url and return it in a structured format
def build_reader_agent():
    return create_agent(
        model = llm,
        tools = [scrape_url],     
    )

# writer chain 
writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert research writer. Write clear, structured and insightful reports."),
    ("human", """Write a detailed research report on the topic below.

Topic: {topic}

Research Gathered:
{research}

Structure the report as:
- Introduction
- Key Findings (minimum 3 well-explained points)
- Conclusion
- Sources (list all URLs found in the research)

Be detailed, factual and professional."""),
])

writer_chain = writer_prompt | llm

#critic_chain 

critic_prompt = ChatPromptTemplate.from_messages([
     ("system", "You are a sharp and constructive research critic. Be honest and specific."),
    ("human", """Review the research report below and evaluate it strictly.

Report:
{report}

Respond in this exact format:

Score: X/10

Strengths:
- ...
- ...

Areas to Improve:
- ...
- ...

One line verdict:
..."""),
])

critic_chain = critic_prompt | llm 




