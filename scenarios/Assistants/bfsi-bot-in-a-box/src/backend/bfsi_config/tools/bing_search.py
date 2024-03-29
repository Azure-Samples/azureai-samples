import requests
from bs4 import BeautifulSoup
import re
import os
from dotenv import load_dotenv
import json
from bfsi_config.tools.open_ai_response import get_ai_resp
from typing import Optional

load_dotenv(override=True)
bing_key = os.getenv("BING_KEY")
bing_endpoint = os.getenv("BING_ENDPOINT")


# add type annotations to the function signature
def get_bing_search_url(search_term: str, freshness: Optional[str] = None) -> list:
    search_url = bing_endpoint
    headers = {"Ocp-Apim-Subscription-Key": bing_key}
    params = {"q": search_term, "textDecorations": True, "textFormat": "HTML"}
    if freshness:
        if freshness in ["Day", "Week", "Month"]:
            params["freshness"] = freshness
        else:
            raise ValueError("freshness must be 'Day', 'Week', or 'Month'")
    response = requests.get(search_url, headers=headers, params=params)

    response.raise_for_status()
    search_results = response.json()
    print(search_results)
    url_list = []

    if "webPages" in search_results:
        top_search_result = search_results["webPages"]["value"][0:1]
        for search_result in top_search_result:
            url_list.append(search_result["url"])
    print(url_list)
    return url_list


def replace_multiple_spaces(text: str) -> str:
    text = re.sub(" +", " ", text)
    return re.sub("\n+", "\n", text)


def load_url_content(url: str) -> str:
    print("in load url content")
    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")
    content = soup.get_text()
    print(content)
    return replace_multiple_spaces(content)


def search_web(query: str, freshness: Optional[str] = None) -> str:
    url_list = get_bing_search_url(query, freshness)
    retval = []
    for url in url_list:
        retval.append(json.dumps({"url": url, "content": load_url_content(url)}))
    return ",".join(retval)
    # print(ret_val)


def search_web_with_freshness_filter(query: str, freshness: str) -> str:
    try:
        search_web(query, freshness)
        system_role = """You answer users query based on input knowledge base."""
        system_content = f"{system_role}"
        system_content = f"{system_content}\nAnswer:"
        print(system_content)
        resp = get_ai_resp(query, system_content)
    except Exception as e:
        print(e)
        error_msg = "Unable to retrieve results at this time. Please try again later."
        resp = error_msg
    return resp
