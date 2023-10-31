from promptflow import tool

@tool
def my_lc_func_tool(question) -> dict:
    return {
        "answer": question
    }