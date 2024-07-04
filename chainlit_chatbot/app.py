import os
import chainlit as cl
from openai import OpenAI
from dotenv import load_dotenv
from langchain.document_loaders import PyPDFLoader
from pptx import Presentation
import logging
from typing import List, Dict

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
    
    # Display a welcome message
    await cl.Message(content="Welcome to your AI assistant! How can I help you today?").send()


@cl.on_message
async def main(message: cl.Message):
    conversation_history: List[Dict[str, str]] = cl.user_session.get("conversation_history", [])
    
    async def process_file(file: cl.File) -> str:
        logger.info(f"Processing file: {file.name}")
        try:
            if file.name.lower().endswith('.pdf'):
                loader = PyPDFLoader(file.path)
                pages = loader.load_and_split()
                file_content = "\n\n".join(page.page_content for page in pages)
                logger.info(f"Extracted {len(pages)} pages from PDF, total length: {len(file_content)} characters")
            elif file.name.lower().endswith(('.ppt', '.pptx')):
                prs = Presentation(file.path)
                file_content = "\n\n".join(shape.text for slide in prs.slides for shape in slide.shapes if hasattr(shape, 'text'))
                logger.info(f"Extracted content from PPT, total length: {len(file_content)} characters")
            else:
                raise ValueError("Unsupported file type. Please upload a PDF or PPT file.")

            if not file_content.strip():
                raise ValueError("No text could be extracted from the file.")
            
            summary_prompt = f"Summarize the following text from a {file.name.split('.')[-1].upper()} file (max 150 words):\n\n{file_content[:4000]}"
            summary_response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": summary_prompt}],
                max_tokens=200
            )
            return summary_response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error processing file: {str(e)}", exc_info=True)
            raise

    if message.elements:
        for element in message.elements:
            if isinstance(element, cl.File) and element.mime in ["application/pdf", "application/vnd.openxmlformats-officedocument.presentationml.presentation"]:
                try:
                    summary = await process_file(element)
                    file_type = "PDF" if element.mime == "application/pdf" else "PPT"
                    conversation_history.append({"role": "system", "content": f"{file_type} Summary: {summary}"})
                    await cl.Message(content=f"📄 File '{element.name}' processed. Here's a summary:\n\n{summary}").send()
                except Exception as e:
                    await cl.Message(content=f"❌ Error processing file: {str(e)}").send()
                return
            else:
                await cl.Message(content="❌ Unsupported file type. Please upload a PDF or PPT file.").send()
                return

    conversation_history.append({"role": "user", "content": message.content})

    response = client.chat.completions.create(
        model="gpt-4",
        messages=conversation_history,
        max_tokens=300
    )

    assistant_message = response.choices[0].message
    conversation_history.append({"role": "assistant", "content": assistant_message.content})
    cl.user_session.set("conversation_history", conversation_history)

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
