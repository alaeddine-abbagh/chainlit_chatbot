import os
import chainlit as cl
from openai import OpenAI
from dotenv import load_dotenv

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
    conversation_history.append({"role": "user", "content": message.content})

    # Generate response using OpenAI
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=conversation_history,
        max_tokens=150
    )

    assistant_message = response.choices[0].message
    conversation_history.append({"role": "assistant", "content": assistant_message.content})
    cl.user_session.set("conversation_history", conversation_history)

    await cl.Message(content=assistant_message.content).send()

@cl.on_file_upload(accept=["text/plain"])
async def handle_file_upload(file: cl.File):
    file_content = file.content.decode("utf-8")
    
    # Add file content to conversation history
    conversation_history = cl.user_session.get("conversation_history")
    conversation_history.append({"role": "system", "content": f"The user has uploaded a file with the following content:\n\n{file_content}"})
    cl.user_session.set("conversation_history", conversation_history)
    
    await cl.Message(content=f"File '{file.name}' has been uploaded and added to the conversation. You can now ask questions about its content.").send()

if __name__ == "__main__":
    cl.run()
