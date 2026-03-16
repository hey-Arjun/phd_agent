from tavily import TavilyClient
from dotenv import load_dotenv
import os

load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")


client = TavilyClient(api_key=TAVILY_API_KEY)


def search_phd_programs(query, max_results=25):

    search_query = f"{query} phd program site:.edu OR site:.ac.uk OR site:.de OR site:.nl OR site:.se OR site:.fi OR site:.no OR site:.dk"

    response = client.search(
        query=search_query,
        search_depth="advanced",
        max_results=max_results
    )

    results = []

    for r in response["results"]:
        results.append({
            "title": r["title"],
            "url": r["url"],
            "content": r["content"]
        })

    return results