import os
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.models import VectorizedQuery
from azure.search.documents.indexes.models import (
    SearchIndex,
    SearchField,
    SearchFieldDataType,
    SimpleField,
    SearchableField,
    VectorSearch,
    VectorSearchProfile,
    HnswAlgorithmConfiguration,
    SemanticSearch,
    SemanticConfiguration,
    SemanticPrioritizedFields,
    SemanticField,
)
import json
from bfsi_config.tools.open_ai_response import get_embeddings

# Use this when running the code in the same directory as open_ai_response.py
# from open_ai_response import get_embeddings
from pathlib import Path

load_dotenv(override=True)

search_endpoint = os.getenv("SEARCH_ENDPOINT")
search_key = os.getenv("SEARCH_KEY")
search_index_name = os.getenv("SEARCH_INDEX_NAME")

cred = AzureKeyCredential(search_key)


def get_index(name: str) -> SearchIndex:
    fields = [
        SimpleField(name="ID", type=SearchFieldDataType.String, key=True),
        SearchableField(
            name="Category",
            type=SearchFieldDataType.String,
            sortable=True,
            filterable=True,
        ),
        SearchableField(
            name="Subcategory",
            type=SearchFieldDataType.String,
            sortable=True,
            filterable=True,
        ),
        SearchableField(name="Category_Subcategory", type=SearchFieldDataType.String),
        SearchField(
            name="Category_Subcategory_Vector",
            type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
            searchable=True,
            vector_search_dimensions=3072,
            vector_search_profile_name="my-vector-config",
        ),
    ]
    vector_search = VectorSearch(
        profiles=[
            VectorSearchProfile(
                name="my-vector-config",
                algorithm_configuration_name="my-algorithms-config",
            )
        ],
        algorithms=[HnswAlgorithmConfiguration(name="my-algorithms-config")],
    )
    semantic_search = SemanticSearch(
        configurations=[
            SemanticConfiguration(
                name="default",
                prioritized_fields=SemanticPrioritizedFields(
                    title_field=None,
                    content_fields=[SemanticField(field_name="Category_Subcategory")],
                ),
            )
        ]
    )
    return SearchIndex(
        name=name,
        fields=fields,
        vector_search=vector_search,
        semantic_search=semantic_search,
    )


def get_intent_documents() -> list:
    file_path = "get_intent_data.json"
    with Path(file_path).open("r") as file:
        intent_data = json.load(file)
    docs = []

    sno = 1
    category_list = intent_data["Category_List"]
    for category_obj in category_list:
        category = category_obj["Category_Name"]
        subcategory_list = category_obj["Subcategory_List"]
        for subcategory in subcategory_list:
            category_subcategory = f"{category}_{subcategory}"
            if 1 == 1:
                print(category_subcategory)
                emb = get_embeddings(category_subcategory)
                json_data = {
                    "ID": str(sno),
                    "Category": category,
                    "Subcategory": subcategory,
                    "Category_Subcategory": category_subcategory,
                    "Category_Subcategory_Vector": emb,
                }
            sno += 1
            docs.append(json_data)
    return docs


def get_result(results: list) -> list:
    sno = 1
    res = []
    for result in results:
        sno = sno + 1
        catg = result["Category"]
        subcatg = result["Subcategory"]
        res.append({"Category": catg, "Subcategory": subcatg})
        if sno == 10:
            break
    return res


def keyword_search(query: str) -> list:
    cred = AzureKeyCredential(search_key)
    search_client = SearchClient(search_endpoint, search_index_name, cred)
    sel_fields = ["Category", "Subcategory"]
    results = search_client.search(search_text=query, select=sel_fields)

    return get_result(results)


def vector_search(query: str) -> list:
    search_client = SearchClient(search_endpoint, search_index_name, cred)
    vector_query = VectorizedQuery(
        vector=get_embeddings(query),
        k_nearest_neighbors=3,
        fields="Category_Subcategory_Vector",
    )

    results = search_client.search(
        vector_queries=[vector_query],
        select=["Category", "Subcategory"],
    )

    return get_result(results)


def hybrid_search(query: str) -> list:
    search_client = SearchClient(search_endpoint, search_index_name, cred)
    vector_query = VectorizedQuery(
        vector=get_embeddings(query),
        k_nearest_neighbors=3,
        fields="Category_Subcategory_Vector",
    )

    results = search_client.search(
        search_text=query,
        vector_queries=[vector_query],
        select=["Category", "Subcategory"],
        query_type="semantic",
        semantic_configuration_name="default",
    )

    return get_result(results)


def main() -> None:
    index_client = SearchIndexClient(search_endpoint, cred)
    index = get_index(search_index_name)
    index_names = index_client.list_index_names()
    if search_index_name not in index_names:
        index_client.create_index(index)

    client = SearchClient(search_endpoint, search_index_name, cred)

    intent_docs = get_intent_documents()

    client.upload_documents(documents=intent_docs)


if __name__ == "__main__":
    main()
