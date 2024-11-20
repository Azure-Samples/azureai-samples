# File Search

File Search augments the Agent with knowledge from outside its model, such as proprietary product information or documents provided by your users. 

To access your files, the file search tool uses the vector store object. Upload your files and create a vector store to contain them. Once the vector store is created, you should poll its status until all files are out of the in_progress state to ensure that all content has finished processing. The SDK provides helpers for uploading and polling. 

### File Sources  
- Uploading local files
- [Coming Soon] Azure Blob Storage

### Basic Agent Setup <br> 
The File Search tool has the same functionality as AOAI Assistants. Microsoft managed search and storage resources are used. 
- Uploaded files get stored in Microsoft managed storage
- A vector store is created using a Microsoft managed search resource

### Standard Agent Setup 
The File Search tool uses the Azure AI Search and Azure Blob Storage resources you connected during agent setup.  
- Uploaded files get stored in your connected Azure Blob Storage account
- Vector stores get created using your connected Azure AI Seach resource
<br> </br>

For both Agent setups, OpenAI handles the entire ingestion process, including automatically parsing and chunking documents, generating and storing embeddings, and utilizing both vector and keyword searches to retrieve relevant content for user queries. 

There is no difference in the code between the two setups; the only variation is in where your files and created vector stores are stored.

## Examples

Run the code samples below and view the output. 

>[!NOTE]
> Be sure that you've [installed the SDK](../../quickstart.md#install-the-sdk-package) for your language.

* [Python](./python-file-search.py)
* [C#](./FileSearch.cs)

## Additional samples

* [Python Quart app](https://github.com/Azure-Samples/azureai-assistant-tool/tree/main/samples/FileSearch)
