from openai import AzureOpenAI
from dotenv import load_dotenv
import streamlit as st
import os
import time
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

load_dotenv()

# Initialize session state variables
if 'assistant_run_complete' not in st.session_state:
    st.session_state['assistant_run_complete'] = False
if 'run' not in st.session_state:
    st.session_state['run'] = None
if 'thread' not in st.session_state:
    st.session_state['thread'] = None
if 'messages' not in st.session_state:
    st.session_state['messages'] = None
if 'file_ids' not in st.session_state:
    st.session_state['file_ids'] = None
if 'assistant_file_id' not in st.session_state:
    st.session_state['assistant_file_id'] = None
if 'content' not in st.session_state:
    st.session_state['content'] = None
if 'uploaded_file_name' not in st.session_state:
    st.session_state['uploaded_file_name'] = None




def display_assistant_response(messages_data):
    if messages_data:
        with st.expander("Assistant Messages", expanded=True):
            st.write("**Assistant's Final Response:**")
            assistant_messages = [msg for msg in messages_data if msg.role == 'assistant']
            if assistant_messages:
                final_message = assistant_messages[0]
                if final_message.content:
                    for content_piece in final_message.content:
                        if hasattr(content_piece, 'text'):
                            st.write(content_piece.text.value)
                        elif hasattr(content_piece, 'error'):
                            st.write(f"**Error:** {content_piece.error.message}")
                else:
                    st.write("No content in the assistant's final message.")
            else:
                st.write("No assistant messages available.")
    else:
        st.write("No messages available.")

def provide_download_and_export(content):
    if content is not None:
        col1, col2 = st.columns(2)

        with col1:
            st.download_button(
                label="Download Outliers CSV",
                data=content,
                file_name='outliers.csv',
                mime='text/csv'
            )

        with col2:
            if st.button("Export to Blob Storage"):
                try:
                    blob_client = container_client.get_blob_client('outliers.csv')
                    blob_client.upload_blob(content, overwrite=True)
                    st.success("File exported to Blob Storage successfully.")
                except Exception as e:
                    st.error(f"An error occurred while exporting to Blob Storage: {e}")
    else:
        st.write("No content available to download or export.")

# Create the title and subheader for the Streamlit page
st.title("Advanced Analyst Assistant")
st.subheader("Upload a CSV and ask your questions:")

# Create placeholders in the sidebar
st.sidebar.header('Configuration')

# Placeholder for Blob Connection String
blob_connection_placeholder = st.sidebar.empty()

container_name_placeholder = st.sidebar.empty()

# Placeholder for Azure OpenAI API Key
azure_api_key_placeholder = st.sidebar.empty()

azure_api_endpoint_placeholder = st.sidebar.empty()

# Placeholder for Model Type selection
model_type_placeholder = st.sidebar.empty()

# Placeholder for Model Type selection
version_placeholder = st.sidebar.empty()



# Update the placeholders with input fields
with blob_connection_placeholder.container():
    blob_connection_string = st.text_input('Blob Connection String', value=os.getenv('AZURE_STORAGE_CONNECTION_STRING'), type = 'password')

with container_name_placeholder.container():
    container_name = st.text_input('Blob Container name', value='anomalies')

with azure_api_key_placeholder.container():
    azure_openai_api_key = st.text_input('Azure OpenAI API Key', value=os.getenv("AZURE_OPENAI_API_KEY"), type='password')

with azure_api_endpoint_placeholder.container():
    azure_api_endpoint = st.text_input('Azure OpenAI Endpoint', value=os.getenv("AZURE_OPENAI_ENDPOINT"), type='password')

with model_type_placeholder.container():
    model_type = st.selectbox('Model Type', options=['gpt-4o', 'gpt-3.5-turbo'])

with version_placeholder.container():
    version = st.selectbox('Version', options=["2024-05-01-preview"])

client = AzureOpenAI(
    azure_endpoint=azure_api_endpoint,
    api_key=azure_openai_api_key,
    api_version=version
)

# Define the metaprompt
metaprompt = st.text_area('Your System Message', height=150, value="""
You are a Risk Detector assistant. You specialize in analyzing CSV files to identify anomalies and outliers.

""")

download_ph = "Save these rows in a CSV file named 'outliers.csv'. Ensure that you save the file with the exact name 'outliers.csv' so that it can be retrieved later."

if st.checkbox('Generate CSV with results'):
    metaprompt += download_ph

# Define the user query/prompt
query = st.text_input("Enter your query here:", "Are there any outliers?")

if st.button('Check Blob connection'):
    try:
        connection_string = blob_connection_string
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        container_name = st.text_input('Your container name', 'anomalies')
        container_client = blob_service_client.get_container_client(container_name)
        st.markdown(''':green-background[Connection to Blob Storage successful.]''')
        # Ensure the container exists
        if not container_client.exists():
            container_client.create_container()
            st.write(f"Container '{container_name}' created successfully.")
    except Exception as e:
        st.error(f"An error occurred while checking the Blob connection: {e}")

# Create a file input for the user to upload a CSV
uploaded_file = st.file_uploader(
    "Upload a CSV", type="csv", label_visibility="collapsed"
)

# If the user has uploaded a file, start the assistant process...
if metaprompt and query and uploaded_file is not None:
    # Check if a new file has been uploaded
    if st.session_state['uploaded_file_name'] != uploaded_file.name:
        # Reset the session state because a new file has been uploaded
        st.session_state['uploaded_file_name'] = uploaded_file.name
        st.session_state['assistant_run_complete'] = False
        st.session_state['run'] = None
        st.session_state['thread'] = None
        st.session_state['messages'] = None
        st.session_state['file_ids'] = None
        st.session_state['assistant_file_id'] = None
        st.session_state['content'] = None

    if not st.session_state['assistant_run_complete']:
        # Create a status indicator to show the user the assistant is working
        placeholder = st.empty()  # Use a placeholder
        with placeholder.container():
            status_box = st.info("Starting work...")

        try:
            # Upload the file to OpenAI
            file = client.files.create(
                file=uploaded_file, purpose="assistants"
            )
            st.session_state['assistant_file_id'] = file.id

            assistant = client.beta.assistants.create(
                model="gpt-4o",  # Replace with your model deployment name.
                instructions=metaprompt,
                tools=[{"type": "code_interpreter"}],
                tool_resources={"code_interpreter": {"file_ids": [file.id]}},
                temperature=1,
                top_p=1
            )
            thread = client.beta.threads.create()
            st.session_state['thread'] = thread

            # Add a user question to the thread
            message = client.beta.threads.messages.create(
                thread_id=thread.id,
                role="user",
                content=query  # Replace this with your prompt
            )

            # Create a run with the new thread
            run = client.beta.threads.runs.create(
                thread_id=thread.id,
                assistant_id=assistant.id,
            )
            st.session_state['run'] = run

            # Check periodically whether the run is done, and update the status
            while run.status != "completed":
                time.sleep(5)
                status_box.info(f"{run.status.title()}...")
                run = client.beta.threads.runs.retrieve(
                    thread_id=thread.id, run_id=run.id
                )

            # Once the run is complete, update the status box and show the content
            status_box.success("Complete")
            placeholder.empty()  # Remove the placeholder to avoid nesting

            messages = client.beta.threads.messages.list(
                thread_id=thread.id
            )
            st.session_state['messages'] = messages.data

            # Display the assistant's final response
            display_assistant_response(st.session_state['messages'])

            st.session_state['assistant_run_complete'] = True

            # Retrieve generated files
            file_ids = []

            for message in messages.data:
                # Check if the message has attachments
                if hasattr(message, 'attachments') and message.attachments:
                    for attachment in message.attachments:
                        # Check if the attachment has a 'file_id' attribute
                        if hasattr(attachment, 'file_id'):
                            file_ids.append(attachment.file_id)
            st.session_state['file_ids'] = file_ids

            # Provide the download and export buttons
            if file_ids:
                # Read the content of the file into memory
                content = client.files.content(file_ids[0]).read()
                st.session_state['content'] = content

                provide_download_and_export(content)
            else:
                st.write("No files generated by the assistant.")

        except Exception as e:
            st.error(f"An error occurred: {e}")
            st.stop()
    else:
        # Assistant has already run, display the results from session state
        display_assistant_response(st.session_state['messages'])
        provide_download_and_export(st.session_state['content'])

    # "Show code" button and expander
    if st.button('Show Thinking Steps'):
        with st.expander("Thinking Steps"):
            if st.session_state['run'] is not None and st.session_state['thread'] is not None:
                try:
                    run_steps = client.beta.threads.runs.steps.list(
                        thread_id=st.session_state['thread'].id,
                        run_id=st.session_state['run'].id  # Use the correct run_id here
                    )

                    for idx, step in enumerate(reversed(run_steps.data)):
                        st.write(f"**Step {idx+1}:**")
                        step_type = step.step_details.type

                        # Handle message creation steps
                        if step_type == 'message_creation':
                            message_id = step.step_details.message_creation.message_id
                            # Retrieve the message content
                            message = client.beta.threads.messages.retrieve(
                                thread_id=st.session_state['thread'].id,
                                message_id=message_id
                            )
                            if message.content:
                                for content_piece in message.content:
                                    if hasattr(content_piece, 'text'):
                                        st.markdown(content_piece.text.value)
                        elif step_type == 'tool_calls':
                            tool_calls = step.step_details.tool_calls
                            for tool_call in tool_calls:
                                code = tool_call.code_interpreter.input
                                st.code(code, language="python")
                                # Display any error messages
                                if hasattr(tool_call.code_interpreter, 'error'):
                                    error_message = tool_call.code_interpreter.error.message
                                    st.write(f"Code Interpreter Error: {error_message}")
                        else:
                            st.write(f"Unknown step type: {step_type}")
                except Exception as e:
                    st.error(f"An error occurred while retrieving thinking steps: {e}")
            else:
                st.write("No run data available.")

    # Optionally, add a reset button to allow the user to start over
    if st.button('Reset'):
        # Clean up files
        if st.session_state['assistant_file_id'] is not None:
            try:
                client.files.delete(st.session_state['assistant_file_id'])
            except Exception as e:
                st.error(f"Error deleting assistant file: {e}")
        if st.session_state['file_ids'] is not None:
            for file_id in st.session_state['file_ids']:
                try:
                    client.files.delete(file_id)
                except Exception as e:
                    st.error(f"Error deleting file {file_id}: {e}")
        # Reset session state
        st.session_state['assistant_run_complete'] = False
        st.session_state['run'] = None
        st.session_state['thread'] = None
        st.session_state['messages'] = None
        st.session_state['file_ids'] = None
        st.session_state['assistant_file_id'] = None
        st.session_state['content'] = None
        st.session_state['uploaded_file_name'] = None
        st.experimental_rerun()
else:
    st.write("Please upload a CSV file to start.")