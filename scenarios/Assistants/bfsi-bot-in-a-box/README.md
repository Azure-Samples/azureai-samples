---
page_type: sample
languages:
- python
products:
- azure-openai
description: Sample Application leveraging Assistant API
---

# Contoso Financial Assistant
![Banner](./readme_assets/banner.jpg)

## Description

This repository contains the backend and frontend code for the Contoso Financials Assistant. 
Contoso Financial Assistant caters to below types of queries:
- Contoso financial financial performance in year 2023
- Contoso financial product lines
- Late EMI related queries for paurchases made using Conto Premier Credit Card 


## Tools

- Code Interpreter
- Custom Function to Categorize User Query
- Data file for interest charged on late EMIs
- Data file for info on Contoso Finacial Product portfolio and financial performance


## Installation

1. Clone the repository.
2. cd azureai-samples\scenarios\Assistants\bfsi-bot-in-a-box\src\backend
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

1. Create AI Search index for user query categorization by executing get_intent_init.py 
python bfsi_config\tools\get_intent_init.py
2. Start the backend server using command flask run --host 0.0.0.0 --port 5007
3. Launch the frontend application by opening `assistant.html` file in your browser.
cd azureai-samples\scenarios\Assistants\bfsi-bot-in-a-box\src\frontend
python -m http.server 8000
Browse to http://localhost:8000/assistant.html
4. Sample conversation:
- Hi
- Can you tell me more about contoso?
- Can you create html table with all details?
- Super, I missed my installment for washing machine last month. 
Do I need to pay interest?
- I have taken loan for 2 years. Every Month I pay 1000. 
If I miss all my payments, how much will I pay finally?
- I need detailed calculation for each month showing 
how you arrived at the final figure.
Can you create html table showing details for each of the 24 months?
- Please show for all months
- Thanks - this is super helpful!
