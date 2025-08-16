import os
import sys
from pathlib import Path

# Add the parent directory to Python path so we can import from tools
sys.path.append(str(Path(__file__).parent.parent))

from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.tools import Tool
from tools.tools import get_profile_url_tavily
from langchain import hub

load_dotenv()

def lookup_linkedin(name: str):
    """
    Lookup a LinkedIn profile URL using a name."""

    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        temperature=0,
        google_api_key=os.getenv("GEMINI_API_KEY"),
    )

    template = """
    given the full name {name} I want you to find the link to their LinkedIn profile page. Your answer. should only contain the URL.
    """

    prompt_template = PromptTemplate(input_variables=["name"], template=template)
    tools_for_agent = [
        Tool(
            name="Crawl Google 4 LinkedIn profile page",
            func=get_profile_url_tavily,
            description="Useful for when you need to lookup a LinkedIn profile page URL from a name",
        )
    ]

    react_prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm=llm, tools=tools_for_agent, prompt=react_prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True)

    result = agent_executor.invoke(
        {"input": prompt_template.format(name=name)}
    )
    linkedin_profile_url = result["output"]
    return linkedin_profile_url


if __name__ == "__main__":
    linkedin_profile_url = lookup_linkedin("Thilak Reddy")
    print(linkedin_profile_url)
    
    