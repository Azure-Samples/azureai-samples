# Advanced Analyst Assistant

This demo app showcases the capabilities of Azure OpenAI Assistants API with Code Interpreter. The frontend is developed with Streamlit.

![Demo](https://github.com/Valentina-Alto/CodeInterpreter-anomalies/blob/main/assets/ezgif-5-697c67b237.gif?raw=true)

## Prerequisites

- Python 3.7 or higher
- Azure OpenAI account with access to at least one chat model (e.g. GPT-4o)
- Azure Blob Storage account (optional, for exporting results)
- Required Python packages listed in `requirements.txt`

## Installation

- **Clone the Repository:**

   ```bash
   git clone https://github.com/Valentina-Alto/CodeInterpreter-anomalies.git
   cd CodeIntepreter-anomalies
   ```

- **Create a .env File:**

   ```bash
    AZURE_OPENAI_ENDPOINT=your-azure-openai-endpoint
    AZURE_OPENAI_API_KEY=your-azure-openai-api-key
    AZURE_STORAGE_CONNECTION_STRING=your-azure-storage-connection-string 
    ```

### Option 1: Run the App Locally

- **Run the streamlit app**
   ```bash
    streamlit run app.py
    ```


### Option 2: Create Docker Image and deploy to a container registry

- **Build Docker Image**
   ```bash
    docker build -t codeassistant:latest .
    ```
- **Login into Azure (or your Container Registry of choice)**
   ```bash
    az login
    az acr login --name your-acr-name
    ```
- **Tag and Push your image**
   ```bash
    docker tag codeassistant:latest <your-acr-name>.azurecr.io/codeassistant:latest
    docker push <your-acr-name>.azurecr.io/codeassistant:latest
    ```

- **Run the container locally**
   ```bash
    docker pull <your-acr-name>.azurecr.io/codeassistant:latest
    docker run -p 8501:8501 <your-acr-name>.azurecr.io/codeassistant:latest
    ```