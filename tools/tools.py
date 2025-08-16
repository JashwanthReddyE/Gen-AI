from langchain_tavily import TavilySearch
import os
from dotenv import load_dotenv

load_dotenv()

def get_profile_url_tavily(name: str):
    """
    Search for a LinkedIn profile URL using Tavily.
    """
    search = TavilySearch(api_key=os.getenv("TAVILY_API_KEY"))
    result = search.run(f"{name}")
    return result