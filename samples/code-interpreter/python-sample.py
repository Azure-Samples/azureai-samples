from openai import AzureOpenAI 
     
client = AzureOpenAI( 
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),   
    api_version="2024-05-01-preview", 
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT") 
    ) 
 
# Upload a file with an "assistants" purpose 
file = client.files.create( 
  file=open("speech.py", "rb"), 
  purpose='assistants' 
) 
 
# Create an assistant using the file ID 
assistant = client.beta.assistants.create( 
  instructions="You are an AI assistant that can write code to help answer math questions.", 
  model="gpt-4-1106-preview", 
  tools=[{"type": "code_interpreter"}], 
  tool_resources={"code interpreter":{"file_ids":[file.id]}} 
) 

client = AzureOpenAI( 
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),   
    api_version="2024-05-01-preview", 
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT") 
    ) 
 
thread = client.beta.threads.create( 
  messages=[ 
    { 
      "role": "user", 
      "content": "I need to solve the equation `3x + 11 = 14`. Can you help me?", 
      "file_ids": ["file.id"] # file id will look like: "assistant-R9uhPxvRKGH3m0x5zBOhMjd2"  
    } 
  ] 
) 