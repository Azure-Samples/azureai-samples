# File Search

File Search augments the Agent with knowledge from outside its model, such as proprietary product information or documents provided by your users. OpenAI automatically parses and chunks your documents, creates and stores the embeddings, and use both vector and keyword search to retrieve relevant content to answer user queries. 

To access your files, the file search tool uses the vector store object. Upload your files and create a vector store to contain them. Once the vector store is created, you should poll its status until all files are out of the in_progress state to ensure that all content has finished processing. The SDK provides helpers for uploading and polling. 

### File Sources  
- Uploading local files
- Files from message attachments
- [coming soon] Azure Blob Storage

### Standard Agent Setup <br> 
The File Search tool has the same functionality as AOAI Assistants. Microsoft managed search and storage resources are used. 
- Uploaded files get stored in Microsoft managed storage
- A vector store is created using Microsoft managed search resources

### Custom Agent Setup <br> 
The File Search tool uses the Azure AI Search and Azure Blob Storage resources you connected during project and agent setup.  
- Uploaded files get stored in your connected Azure Blob Storage account.  
- Vector stores get created using your connected Azure AI Seach resource. 

## Examples

Run the code samples below and view the output. 

>[!NOTE]
> Be sure that you've [installed the SDK](../../quickstart.md#install-the-sdk-package) for your language.

* [Python](./python-file-search.py)

## Additional samples

* [Python Quart app](https://github.com/Azure-Samples/azureai-assistant-tool/tree/main/samples/FileSearch)
