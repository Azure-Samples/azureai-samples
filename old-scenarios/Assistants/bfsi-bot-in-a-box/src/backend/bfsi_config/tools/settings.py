from bfsi_config.tools.bing_search import search_web_with_freshness_filter
from bfsi_config.tools.get_intent import categorize_user_query

assistant_name = "contoso-assistant"

func_list = {
    "search_web_with_freshness_filter": search_web_with_freshness_filter,
    "categorize_user_query": categorize_user_query,
}

tools_list = [
    {"type": "code_interpreter"},
    # {"type": "retrieval"},
    {
        "type": "function",
        "function": {
            "name": "search_web_with_freshness_filter",
            "module": "functions.user_functions",
            "description": """Generates response to the query using knowledgebase 
            it retrives by searching the web for information related to the input 
            query and filters results by freshness if specified.""",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query to look for information on the web.",
                    },
                    "freshness": {
                        "type": "string",
                        "description": """The time frame filter for search results. 
                        Acceptable values are 'Day', 'Week', or 'Month'.""",
                        "enum": ["Day", "Week", "Month"],
                    },
                },
                "required": ["query"],
            },
            "returns": {
                "type": "string",
                "description": "Response to the query on the basis of web search.",
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "categorize_user_query",
            "module": "functions.user_functions",
            "description": "Determines and returns the Category & Subcategory for the input user query.",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_query": {
                        "type": "string",
                        "description": "Full user query for which categorization needs to be determined",
                    }
                },
                "required": ["user_query"],
            },
            "returns": {
                "type": "string",
                "description": "String containing Category & Subcategory for the input query",
            },
        },
    },
]
