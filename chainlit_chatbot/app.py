import os
import chainlit as cl
from openai import OpenAI
from dotenv import load_dotenv
from langchain.document_loaders import PyPDFLoader
import logging
from typing import List, Dict

# Set up logging for debugging purposes
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client with API key from environment variables
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Custom CSS to make the app more visually appealing
custom_css = """
<style>
    .chat-message { 
        border-radius: 10px; 
        padding: 10px; 
        margin-bottom: 10px; 
        max-width: 80%;
    }
    .user-message { 
        background-color: #e6f3ff; 
        align-self: flex-end; 
    }
    .assistant-message { 
        background-color: #f0f0f0; 
        align-self: flex-start; 
    }
</style>
"""

@cl.on_chat_start
async def start():
    # Initialize an empty conversation history when a new chat starts
    cl.user_session.set("conversation_history", [])
    
    # Set the logo for the chat interface
    await cl.set_chat_profiles([
        cl.ChatProfile(
            name="AI Assistant",
            image="https://img.freepik.com/vecteurs-libre/vecteur-degrade-logo-colore-oiseau_343694-1365.jpg?size=626&ext=jpg",  # Replace with your actual logo URL
            markdown_description="I'm your sophisticated AI assistant, ready to help with various tasks!"
        )
    ])
    
    # Display a welcome message with custom CSS
    await cl.Message(
        content="Welcome to your sophisticated AI assistant! How can I help you today?",
        elements=[cl.Text(name="custom_css", content=custom_css)]
    ).send()


@cl.on_message
async def main(message: cl.Message):
    conversation_history: List[Dict[str, str]] = cl.user_session.get("conversation_history", [])
    
    async def process_pdf(file: cl.File) -> str:
        logger.info(f"Processing PDF file: {file.name}")
        try:
            loader = PyPDFLoader(file.path)
            pages = loader.load_and_split()
            
            file_content = "\n\n".join(page.page_content for page in pages)
            logger.info(f"Extracted {len(pages)} pages, total length: {len(file_content)} characters")
            
            if not file_content.strip():
                raise ValueError("No text could be extracted from the PDF.")
            
            summary_prompt = f"Summarize the following text from a PDF (max 150 words):\n\n{file_content[:4000]}"
            summary_response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": summary_prompt}],
                max_tokens=200
            )
            return summary_response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error processing PDF: {str(e)}", exc_info=True)
            raise

    if message.elements:
        for element in message.elements:
            if isinstance(element, cl.File) and element.mime == "application/pdf":
                try:
                    summary = await process_pdf(element)
                    conversation_history.append({"role": "system", "content": f"PDF Summary: {summary}"})
                    await cl.Message(content=f"📄 File '{element.name}' processed. Here's a summary:\n\n{summary}").send()
                except Exception as e:
                    await cl.Message(content=f"❌ Error processing file: {str(e)}").send()
                return
            else:
                await cl.Message(content="❌ Unsupported file type. Please upload a PDF file.").send()
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

    await cl.Message(content=assistant_message.content, elements=[
        cl.Text(name="custom_css", content=custom_css)
    ]).send()

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
