import requests
import os
from dotenv import load_dotenv

load_dotenv()

def scrape_linkedin_profile(gist_linkedin_profile_url: str, mock: bool = False):
    """
    Scrape the LinkedIn profile URL and return the profile data.
    """
    if mock:
        gist_linkedin_profile_url = "https://gist.githubusercontent.com/thilakreddy4304/2b5a8d87b9dd47f4c2629da876237e13/raw/1b8d3fd86c282e1af786536fdc5cb147ccfde1b8/thilak-reddy-scraping.json"
        response = requests.get(
            gist_linkedin_profile_url,
            timeout=10,
        )
    else:
        api_endpoint = "https://api.scrapin.io/enrichment/profile"
        params = {
            "apikey": os.environ["SCRAPIN_API_KEY"],
            "linkedInUrl": gist_linkedin_profile_url,
        }
        response = requests.get(
            api_endpoint,
            params=params,
            timeout=10,
        )

    data = response.json().get("person")
    data = {
        k: v
        for k, v in data.items()
        if v not in ([], "", "", None) and k not in ["certifications"]
    }

    return data

# if __name__ == "__main__":
#     linkedin_profile_url = "https://www.linkedin.com/in/thilakreddy/"
#     print(scrape_linkedin_profile(linkedin_profile_url))