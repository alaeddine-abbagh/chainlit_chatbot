import os
import chainlit as cl
from openai import OpenAI
from dotenv import load_dotenv
from langchain.document_loaders import PyPDFLoader
import tempfile
import logging

# Set up logging for debugging purposes
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client with API key from environment variables
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@cl.on_chat_start
async def start():
    # Initialize an empty conversation history when a new chat starts
    cl.user_session.set("conversation_history", [])


@cl.on_message
async def main(message: cl.Message):
    # Retrieve the conversation history from the user session
    conversation_history = cl.user_session.get("conversation_history")
    files = None  # Initialize files variable (not used in current implementation)
 
    # Check if a file was uploaded with the message
    if message.elements:
        for element in message.elements:
            if isinstance(element, cl.File):
                file = element
                print(f"File MIME type: {file.mime}")
                logger.info(f"File path: {file.path}")
                
                try:
                    # Process PDF files
                    if file.mime == "application/pdf":
                        file_content = ""
                        try:
                            # Use PyPDFLoader to extract text from the PDF using its path
                            loader = PyPDFLoader(file.path)
                            pages = loader.load_and_split()
                            
                            logger.info(f"Number of pages in PDF: {len(pages)}")
                            for i, page in enumerate(pages):
                                file_content += page.page_content + "\n\n"
                                logger.info(f"Page {i+1} extracted text length: {len(page.page_content)} characters")

                            os.unlink(temp_file_path)  # Delete the temporary file
                            logger.info(f"Temporary file deleted: {temp_file_path}")
                        except Exception as e:
                            logger.error(f"An error occurred while processing the PDF: {str(e)}", exc_info=True)
                            await cl.Message(content=f"An error occurred while processing the PDF: {str(e)}").send()
                            return
                        
                        if not file_content.strip():
                            logger.warning("No text could be extracted from the PDF. It might be scanned or contain only images.")
                            await cl.Message(content="No text could be extracted from the PDF. It might be scanned or contain only images.").send()
                            return
                        
                        logger.info(f"Total extracted text length: {len(file_content)} characters")
                        
                        # Summarize file content using OpenAI's GPT-3.5-turbo
                        summary_prompt = f"Summarize the following text from a PDF (max 150 words):\n\n{file_content[:4000]}"
                        summary_response = client.chat.completions.create(
                            model="gpt-3.5-turbo",
                            messages=[{"role": "user", "content": summary_prompt}],
                            max_tokens=200
                        )
                        summary = summary_response.choices[0].message.content
                        
                        # Add file summary to conversation history
                        conversation_history.append({"role": "system", "content": f"PDF Summary: {summary}"})
                        cl.user_session.set("conversation_history", conversation_history)
                        
                        await cl.Message(content=f"File '{file.name}' has been processed. Here's a summary:\n\n{summary}").send()
                        return
                    else:
                        await cl.Message(content=f"Unsupported file type: {file.mime}. Please upload a PDF file.").send()
                        return
                except Exception as e:
                    await cl.Message(content=f"An error occurred while processing the file: {str(e)}").send()
                    return

            # This block is unreachable in the current implementation
            # Summarize file content
            summary = generate_summary(file_content)
            
            # Add file summary to conversation history
            conversation_history.append({"role": "system", "content": f"The user has uploaded a file. Here's a summary of its content:\n\n{summary}"})
            cl.user_session.set("conversation_history", conversation_history)
            
            await cl.Message(content=f"File '{file.name}' has been uploaded and summarized. Here's a summary:\n\n{summary}\n\nYou can now ask questions about its content.").send()
            return

    # If no file was uploaded, process the user's message
    conversation_history.append({"role": "user", "content": message.content})

    # Generate response using OpenAI's GPT-4
    response = client.chat.completions.create(
        model="gpt-4",
        messages=conversation_history,
        max_tokens=150
    )

    # Extract the assistant's message from the response
    assistant_message = response.choices[0].message
    # Add the assistant's response to the conversation history
    conversation_history.append({"role": "assistant", "content": assistant_message.content})
    # Update the conversation history in the user session
    cl.user_session.set("conversation_history", conversation_history)

    # Send the assistant's response back to the user
    await cl.Message(content=assistant_message.content).send()

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

if __name__ == "__main__":
    # Run the Chainlit app
    cl.run()
