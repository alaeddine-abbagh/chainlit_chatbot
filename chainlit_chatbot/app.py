# Chainlit Crash Course: Building Conversational AI Applications

import os
import chainlit as cl  # Import the Chainlit library
from openai import OpenAI
from dotenv import load_dotenv
from langchain.document_loaders import PyPDFLoader
from pptx import Presentation
import csv
import io
import logging
from typing import List, Dict, Tuple
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Set up logging for debugging purposes
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client with API key from environment variables
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Chainlit Concept: Chat Start Event
# This function is called when a new chat session starts
@cl.on_chat_start
async def start():
    # Initialize an empty conversation history when a new chat starts
    cl.user_session.set("conversation_history", [])
    
    # Chainlit Concept: Sending Messages
    # Use cl.Message to send a message to the user
    await cl.Message(content="Welcome to your AI assistant! How can I help you today?").send()

# Chainlit Concept: Message Handler
# This function is called every time a user sends a message
@cl.on_message
async def main(message: cl.Message):
    # Chainlit Concept: User Session
    # Retrieve conversation history from the user's session
    conversation_history: List[Dict[str, str]] = cl.user_session.get("conversation_history", [])
    
    # Helper function to process uploaded files
    async def process_file(file: cl.File) -> Tuple[str, str]:
        logger.info(f"Processing file: {file.name}")
        try:
            # Process different file types (PDF, PPT, CSV)
            if file.name.lower().endswith('.pdf'):
                # ... (PDF processing code)
            elif file.name.lower().endswith(('.ppt', '.pptx')):
                # ... (PPT processing code)
            elif file.name.lower().endswith('.csv'):
                # ... (CSV processing code)
            else:
                raise ValueError("Unsupported file type. Please upload a PDF, PPT, or CSV file.")

            if not file_content.strip():
                raise ValueError("No content could be extracted from the file.")
        
            return file_content
        except Exception as e:
            logger.error(f"Error processing file: {str(e)}", exc_info=True)
            raise

    # Chainlit Concept: Handling File Uploads
    # Check if the message contains any uploaded files
    if message.elements:
        for element in message.elements:
            if isinstance(element, cl.File) and (element.mime in ["application/pdf", "application/vnd.openxmlformats-officedocument.presentationml.presentation", "text/csv"] or element.name.lower().endswith('.csv')):
                try:
                    file_content, summary = await process_file(element)
                    file_type = "PDF" if element.mime == "application/pdf" else "PPT" if element.mime == "application/vnd.openxmlformats-officedocument.presentationml.presentation" else "CSV"
                    conversation_history.append({"role": "system", "content": f"{file_type} Content: {file_content}\n\nSummary: {summary}"})
                    await cl.Message(content=f"📄 File '{element.name}' processed. Here's a summary:\n\n{summary}\n\nYou can now ask questions about this document.").send()
                except Exception as e:
                    await cl.Message(content=f"❌ Error processing file: {str(e)}").send()
                return
            else:
                await cl.Message(content="❌ Unsupported file type. Please upload a PDF, PPT, or CSV file.").send()
                return

    # Add user message to conversation history
    conversation_history.append({"role": "user", "content": message.content})

    # Generate response using OpenAI
    response = client.chat.completions.create(
        model="gpt-4",
        messages=conversation_history,
        max_tokens=300
    )

    # Extract assistant's reply
    assistant_message = response.choices[0].message
    conversation_history.append({"role": "assistant", "content": assistant_message.content})
    
    # Chainlit Concept: Updating User Session
    # Store the updated conversation history in the user's session
    cl.user_session.set("conversation_history", conversation_history)

    # Send the assistant's reply to the user
    await cl.Message(content=assistant_message.content).send()

# Helper function to generate summaries
def generate_summary(text):
    """
    Generate a summary of the given text using OpenAI's GPT-4 model.
    
    :param text: The text to summarize
    :return: A summary of the text
    """
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes documents."},
            {"role": "user", "content": f"Please summarize the following text in about 3-4 sentences:\n\n{text}"}
        ],
        max_tokens=150
    )
    return response.choices[0].message.content

# Chainlit Concept: Running the App
if __name__ == "__main__":
    # Run the Chainlit app
    cl.run()
