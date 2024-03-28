from assistant_config.func_get_intent_init import hybrid_search
from assistant_config.open_ai_response import get_ai_resp


def categorize_user_query(user_query: str) -> str:
    print(user_query)
    knowledgebase = hybrid_search(user_query)
    print(knowledgebase)
    system_role = """You identify Category and Subcategory for the input 
    customer query from the possible values in input knowledge base. 
    You share the output as json."""
    output_json = {
        "Category": "<value of best matching Category>",
        "Subcategory": "<value of 1st best Subcategory for best matching Category>",
    }
    system_content = f"{system_role}\n"
    system_content = f"{system_content}Output Json:\n{output_json}\n"
    system_content = f"{system_content}Knowledge Base:\n{knowledgebase}\n"

    resp = get_ai_resp(user_query, system_content)
    print(resp)
    return resp
