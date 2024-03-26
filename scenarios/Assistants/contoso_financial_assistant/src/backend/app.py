# app.py
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
    clean_assistants,
    clean_files,
)
from create_assistant import (
    get_step_details,
    poll_run_till_completion,
    retrieve_and_print_messages,
)
from open_ai_response import client

# clean_assistants()
# clean_files()
cache = {}
verbose_output = False
assistant_name = "bfsi-assistant"
instructions = """You are an assistant designed to help answer customer queries.
\n -------------
\nYou handle only following type of queries:
\n1. Questions related to the products offered by Contoso Financials.
\n2. Questions related to performance of Contoso Financials company.
\n2. Latest financial news across the globe.
\n3. Late EMI payment related queries. 
\n
\n -------------
\nYou follow below mentioned guidelines to answer user queries:
\n1. Responses should be concise, simple, clear and easy to understand.
\n2. Enable user to get answers in minimal iterations.
\n3. If the text response is long, organize it as list of points for better readability.
\n4. Do not have non ascii characters in the response.
\n5. If any table data is requested, present it in the form of a tabular chart image.
\n6. If you create an image, do NOT have the image url in the response for the user to download.
\n7. If the user thanks you, you revert with a summary, category & subcategory of the conversation 
\n8. You Identify category and sub-category using func categorize_user_query only after user thanks.
\n9. Interest is compounded monthly. All your calculations should be accurate. 
\n10. Ex - Miss EMI of 1000, interest 5% per month, next month EMI 1000, so Net amt due:2050.
\n -------------
You use below mentioned data sources depending on the category of the query: 
\n 1. Use search_web_with_freshness_filter for latest financial news.
\n 2. For Contoso Financials performance and product portfolio, refer to PDF file - contoso.pdf.
\n 4. Interest rates on late EMI is in csv file - late_emi_interest.csv.
\n -------------
\nYou leverage code interpreter tool wherever necessary to execute code snippets and provide responses.
"""
available_functions = {
    "search_web_with_freshness_filter": search_web_with_freshness_filter,
    "categorize_user_query": categorize_user_query,
}


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
        wait=0.5,
    )

    if status == 1:
        final_response = retrieve_and_print_messages(client=client, thread_id=thread.id)
    else:
        final_response = []
        print("error in getting answer for query")

    # final_response.append({"Step Details" :  get_step_details(run, thread)})
    return {"messages": final_response, "thread_id": thread.id, "run_id": run.id}


clean_assistants()
clean_files()
assistant_files = upload_file()
for filename in assistant_files:
    instructions = instructions.replace(filename, assistant_files[filename])
# print(instructions)
file_ids = list(assistant_files.values())

assistant = create_assistant(assistant_name, instructions, tools_list, file_ids)
app = Flask(__name__)
CORS(app)


# add type annotations to the function signature
@app.route("/get_step", methods=["POST"])
def api_get_step() -> dict:
    thread_id = request.form.get("thread_id")
    run_id = request.form.get("run_id")

    if thread_id == "":
        return None

    run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
    thread = client.beta.threads.retrieve(thread_id)
    step_list, step_id_list = get_step_details(run, thread)
    return {"step_list": step_list, "step_id_list": step_id_list}


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
