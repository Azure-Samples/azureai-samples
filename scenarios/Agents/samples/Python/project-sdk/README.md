# Azure Agents Samples - Python Project SDK

## Tools

### Code Interpreter

* [Code Interpreter tool sample](./code-interpreter.py)

The Code Interpreter tool allows the Agent to write and execute Python code in a sandboxed environment. With the Code Interpreter enabled, your Agent can iteratively run code to solve complex coding, mathematical, and data analysis problems.

### File Search

* [File Search tool sample](./file-search.py)
File Search augments the Agent with knowledge from outside its model, such as proprietary product information or documents provided by your users.

To access your files, the file search tool uses the vector store object. Upload your files and create a vector store to contain them. Once the vector store is created, you should poll its status until all files are out of the in_progress state to ensure that all content has finished processing. The SDK provides helpers for uploading and polling.
