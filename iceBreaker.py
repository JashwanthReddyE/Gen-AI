import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from third_parties.linkedin import scrape_linkedin_profile
from agents.linkedin_lookup_agent import lookup_linkedin
from output_parsers import summary_parser

load_dotenv()

def ice_break_with(name: str):
    """
    Ice break with a person using their LinkedIn profile.
    """

    linkedin_profile_url = lookup_linkedin(name)
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url)

    summary_template = """
    given the Linkedin information {information} about a person I want you to create:
    1. A short summary
    2. two interesting facts about them
    \n{format_instructions}
    """
    summary_prompt_template = PromptTemplate(
        input_variables=["information"], 
        template=summary_template,
        partial_variables={"format_instructions": summary_parser.get_format_instructions()})

    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=os.getenv("GEMINI_API_KEY"),
    )

    chain = summary_prompt_template | llm | summary_parser
    res = chain.invoke({"information": linkedin_data})
    return res


if __name__ == "__main__":
    print("Ice Breaker Entered")
    print(ice_break_with("Thilak Reddy United States"))