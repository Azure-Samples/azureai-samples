# from bfsi_config.tools.get_intent_init import hybrid_search
# from bfsi_config.tools.open_ai_response import get_ai_resp

from bfsi_config.tools.get_intent_init import hybrid_search
from bfsi_config.tools.open_ai_response import get_ai_resp


def categorize_user_query(user_query: str) -> str:
    # print(user_query)
    knowledgebase = hybrid_search(user_query)
    # print(knowledgebase)
    system_role = """You identify Category and Subcategory for the input 
    customer query from the possible values in input knowledge base. 
    """

    system_content = f"{system_role}\n"
    system_content = f"{system_content}Knowledge Base:\n{knowledgebase}\n"

    resp = get_ai_resp(user_query, system_content)
    print(resp)
    return resp


# if __name__ == "__main__":
#    categorize_user_query(" I missed my first EMI on EMI Card. How much do a pay now?")
