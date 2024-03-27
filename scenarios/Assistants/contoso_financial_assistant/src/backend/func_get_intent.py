from create_intent_index import hybrid_search
from open_ai_response import get_ai_resp


def categorize_user_query(user_query: str) -> str:
    knowledgebase = hybrid_search(user_query)
    # print(knowledgebase)
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

    return get_ai_resp(user_query, system_content)
    # print(resp)
