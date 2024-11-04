# File Search

File Search augments the Agent with knowledge from outside its model, such as proprietary product information or documents provided by your users. OpenAI automatically parses and chunks your documents, creates and stores the embeddings, and use both vector and keyword search to retrieve relevant content to answer user queries. 

To access your files, the file search tool uses the vector store object. Upload your files and create a vector store to contain them. Once the vector store is created, you should poll its status until all files are out of the in_progress state to ensure that all content has finished processing. The SDK provides helpers for uploading and polling. 

## Examples

Run the code samples below and view the output. 

>[!NOTE]
> Be sure that you've installed the [correct SDK](../../quickstart.md#install-the-sdk-package) for your language.

* [Python](./python-sample.py)

## Additional samples

* [Python Quart app](https://github.com/Azure-Samples/azureai-assistant-tool/tree/main/samples/FileSearch)