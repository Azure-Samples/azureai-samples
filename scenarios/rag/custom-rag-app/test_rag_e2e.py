# ruff: noqa: ANN201

# Tests running of the custom rag app end-to-end
#


def test_chat_with_products():
    from create_search_index import create_index_from_csv

    create_index_from_csv("products", "assets/products.csv")

    from chat_with_products import chat_with_products

    response = chat_with_products(
        messages=[{"role": "user", "content": "what kind of tents would you recommend for 4 people?"}]
    )
    print(response)
