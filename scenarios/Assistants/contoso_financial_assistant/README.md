# Contoso Financial Assistant

![Contoso Financials](media/ContosoFinancials.jpg)

## Description

This repository contains the backend and frontend code for the Contoso Financials Assistant. It is designed to provide financial assistance to users by leveraging various technologies. It caters to below types of queries
- Contoso financial financial performance in year 2023
- Contoso financial product lines
- Late EMI related queries for paurchases made using Conto Premier Credit Card 


## Backend - Tools and Functionalities

### Code Interpreter

- **Dynamic Response Generation:** This tool is leveraged for generating dynamic responses to queries that require real-time data processing or when a custom response generation is necessary, ensuring flexibility and adaptability in handling user requests.

### Web Search with Freshness Filter

- **Integration with Bing's Search API:** This feature leverages Bing's search API to find web content related to a user's query, enriching the data available for response generation. This is optional feature.

### Categorize User Query

- **AI-Powered Categorization:** Utilizing AI Search and Azure Open AI, this functionality determines the most relevant category and subcategory for a given user query.


## Integration and Workflow

### User Query Processing

Depending on the type of query, the backend may:
- Perform a web search using Bing's API for up-to-date information.
- Access local data files for static data.
- Invoke the code interpreter for dynamic data processing, catering to a wide range of informational and transactional queries.

### Response Generation

For complex queries or those requiring bespoke responses, the backend utilizes Azure OpenAI's capabilities to generate coherent and contextually accurate responses. This allows the Contoso Financials Assistant to address a wide range of financial queries with sophisticated understanding.

### Integration with Frontend

The processed responses are then formatted and sent back to the frontend application, where they are presented to the user in an easily digestible format. This ensures that users receive information that is not only accurate but also accessible and actionable, enhancing overall user experience.

## Frontend: 
Frontend application is a basic HTML, CSS, and JavaScript app.
The main file in this project is `assistant.html`.

## Installation

1. Clone the repository.
2. Install the necessary dependencies for the backend using requirements.txt
3. Create a .env file in backend folder and specify values of following variables
      OPEN_AI_EMBEDDING_ENDPOINT=<your_open_ai_embedding_endpoint>
      OPEN_AI_EMBEDDING_KEY=<your_open_ai_embedding_key>
      OPEN_AI_EMBEDDING_DEPLOYMENT_NAME=<your_open_ai_embedding_deployment_name>
      
      OPEN_AI_ENDPOINT=<your_open_ai_endpoint>
      OPEN_AI_KEY=<your_open_ai_key>
      OPEN_AI_DEPLOYMENT_NAME=<your_open_ai_deployment_name>
      
      SEARCH_ENDPOINT=<your_search_endpoint>
      SEARCH_KEY=<your_search_key>
      SEARCH_INDEX_NAME=<your_search_index_name>
      
      BING_KEY=<your_bing_key>
      BING_ENDPOINT=<your_bing_endpoint>

## Usage

1. Create AI Search index for user query categorization by executing func_get_intent_init.py 
2. Start the backend server using command flask run --host 0.0.0.0 --port 5007
3. Launch the frontend application by opening `assistant.html` file in your browser.
4. Sample conversation:
I purchased a washing machine on EMI Premier card. 
I was to pay an emi of 1000 rs every month for a period on 1 year.. 
I missed my first EMI due last month. How much do i pay this month?
OR 
can you tell me about performance of contoso financials in 2023?



## Contributing

Contributions are welcome! If you would like to contribute to this project, please follow the guidelines outlined in [CONTRIBUTING.md](path/to/CONTRIBUTING.md).

## License

This project is licensed under the [MIT License](path/to/LICENSE).

## Contact

If you have any questions or suggestions, feel free to reach out to us at [shagrawal@microsoft.com](mailto:shagrawal@microsoft.com).