# Fine-tuning with function calling - stock price use case
This repo demonstrates the utility of function calling with fine-tuned models. We want to build a chatbot that retrieves stock prices from an external API, in response to user inquiries. With just the base model, we identified two challenges: (1) the model does a poor job at distinguishing real companies from fake, and (2) our function calling definitions were very long – and increased our tokens per prompt dramatically. We’ll explore how we can use fine tuning, with function calling, to improve the model’s accuracy and performance. 

Fine tuning GPT-35-turbo-1106 and GPT-35-turbo-0613 models with function calling is a straightforward process outlined in the [documentation](https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/fine-tuning?tabs=turbo%2Cpython&pivots=programming-language-studio). Utilize the Create custom model wizard to select the model, configure hyperparameters, and initiate training. After successful fine-tuning, deploy the model, providing a deployment name, and monitor progress in Azure OpenAI Studio. Once deployed, utilize the Azure OpenAI endpoint for inference by including the model name, functions, and function calls in the completion requests.

Once we’ve created a fine tuned model that meets our needs, we'll put it all together by developing a basic application that allows users to check stock prices for different companies. We will use YFinance Python library for easy retrieval of current stock prices. 

We will show you three notebooks as follows:

**fine-tuning with function calling-inference-hallucination scenario.ipynb** demonstrates how to address hallucination using a fine-tuned model with function calling.

**fine-tuning with function calling-inference-token reduction scenario.ipynb** illustrates how to reduce token usage using a fine-tuned model with function calling.

Finally, **fine-tuning with function calling-e2e.ipynb** showcases the utilization of a fine-tuned function calling model in an end-to-end application.

Please note, in all these examples, we assumed you already fine-tuned your model using the datasets shared in this repo. 

