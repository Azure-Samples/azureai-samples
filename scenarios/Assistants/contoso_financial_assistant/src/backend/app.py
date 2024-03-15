from flask import Flask, request
from flask_cors import CORS

from assistant_tools import tools_list
from func_bing_search import search_web_with_freshness_filter
from func_get_intent import categorize_user_query
from create_assistant import (
    upload_file,
    create_assistant,
    create_thread,
    create_message,
)
from create_assistant import (
    get_step_details,
    poll_run_till_completion,
    retrieve_and_print_messages,
)
from open_ai_response import client

# clean_assistants()
# clean_files()

assistant_name = "bfsi-assistant"
instructions = """You are an assistant designed to help answer customer queries.
\n0. You keep answers concise, simple and easy to understand with only alpha 
numeric characters. You try to close convesation with minimum roundtrip queries.
\n1. You cater to only queries around Contoso Financial Products or  latest financial 
news across the globe including currency exchange rates, stock market indices etc..
\n2. You call search_web_with_freshness_filter only user is asking about latest financial 
news or currency exchange rates or stock market news. 
\n2.1. You identify Category and Sub Category of the user query.
\n3. If the user query is around interest charged on late EMI payment, 
you get interest rate info from late_emi_interest.csv file uploaded.
\n4. If user misses EMI, then interest will be charged on the net amount 
due including EMI missed and interest till date.
\n5. The output json needs to have four keys in json: Category, Sub_Category, 
Summary_Of_User_Query, Response_of_User_Query)
\n6. If user query is not related to Contoso Financial Products or 
you are not able to determine Category or Sub_Category, you return Response indicating the same.
\n7. The final output is a json with above mentioned keys .
\n8. The value of key Response_of_User_Query should be the text that can be reverted to the user.
\n9. When ever asked about tabular data, create a tabular chart image. 
\10. Make sure all you responses are consistent and clear, accurate, 
concise and enable answer to user's query in minimum iterations.
\11. For info around Contoso Financials company, its performance and 
product portfoloio, you answer questions based on the pdf file that has been uploaded. 
\12. The pdf file uploaded has info about Contoso Financials 
"""

available_functions = {
    "search_web_with_freshness_filter": search_web_with_freshness_filter,
    "categorize_user_query": categorize_user_query,
}
# available_functions = {"categorize_user_query":categorize_user_query}
verbose_output = False
file_ids = upload_file()
assistant = create_assistant(assistant_name, instructions, tools_list, file_ids)


# add type annotations to the function signature
def get_answer_for_query(user_query: str, thread_id: str) -> dict:
    message = {"role": "user", "content": user_query}
    thread = create_thread(thread_id)
    create_message(client, thread.id, message["role"], message["content"])

    run = client.beta.threads.runs.create(
        thread_id=thread.id, assistant_id=assistant.id, instructions=instructions
    )
    status = poll_run_till_completion(
        client=client,
        thread_id=thread.id,
        run_id=run.id,
        available_functions=available_functions,
        max_steps=20,
        wait=5,
    )

    if status == 1:
        final_response = retrieve_and_print_messages(client=client, thread_id=thread.id)
    else:
        final_response = []
        print("error in getting answer for query")

    # final_response.append({"Step Details" :  get_step_details(run, thread)})
    return {"messages": final_response, "thread_id": thread.id, "run_id": run.id}


app = Flask(__name__)
CORS(app)


# add type annotations to the function signature
@app.route("/get_step", methods=["POST"])
def api_get_step() -> dict:
    prv_step_id_list = request.form.get("prv_step_id_list")
    # prv_step_id_list = prv_step_id_list.split(",")
    thread_id = request.form.get("thread_id")
    run_id = request.form.get("run_id")

    if thread_id == "":
        return None

    run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
    thread = client.beta.threads.retrieve(thread_id)
    step_list, step_id_list = get_step_details(run, thread, prv_step_id_list)
    return {"step_list": step_list, "step_id_list": step_id_list}


cache = {}


@app.route("/get_answer", methods=["POST"])
def api_get_answer() -> dict:
    query = request.form.get("query")
    thread_id = request.form.get("thread_id")
    if thread_id == "":
        thread_id = None
    if query in cache:
        print("Returning cached response.")
        return cache[query]

    response = get_answer_for_query(query, thread_id)
    print(response)
    cache[query] = response

    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5007)
