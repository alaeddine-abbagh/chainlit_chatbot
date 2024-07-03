import os
import chainlit as cl
from openai import OpenAI
from dotenv import load_dotenv
import PyPDF2
import io

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@cl.on_chat_start
async def start():
    cl.user_session.set("conversation_history", [])


@cl.on_message
async def main(message: cl.Message):
    conversation_history = cl.user_session.get("conversation_history")

    # Check if a file was uploaded
    if message.elements:
        for element in message.elements:
            if isinstance(element, cl.File):
                file = element
                if file.mime == "text/plain":
                    file_content = file.content.decode("utf-8")
                elif file.mime == "application/pdf":
                    pdf_reader = PyPDF2.PdfReader(io.BytesIO(file.content))
                    file_content = ""
                    for page in pdf_reader.pages:
                        file_content += page.extract_text()
                else:
                    await cl.Message(content=f"Unsupported file type: {file.mime}").send()
                    return

                # Summarize file content
                summary = generate_summary(file_content)
                
                # Add file summary to conversation history
                conversation_history.append({"role": "system", "content": f"The user has uploaded a file. Here's a summary of its content:\n\n{summary}"})
                cl.user_session.set("conversation_history", conversation_history)
                
                await cl.Message(content=f"File '{file.name}' has been uploaded and summarized. Here's a summary:\n\n{summary}\n\nYou can now ask questions about its content.").send()
                return

    conversation_history.append({"role": "user", "content": message.content})

    # Generate response using OpenAI
    response = client.chat.completions.create(
        model="gpt-4",  # Changed to GPT-4
        messages=conversation_history,
        max_tokens=150
    )

    assistant_message = response.choices[0].message
    conversation_history.append({"role": "assistant", "content": assistant_message.content})
    cl.user_session.set("conversation_history", conversation_history)

    await cl.Message(content=assistant_message.content).send()

def generate_summary(text):
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
    cl.run()
