import os
import chainlit as cl
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Initialize conversation history
conversation_history = []

@cl.on_chat_start
def start():
    cl.user_session.set("conversation_history", [])

@cl.on_message
async def main(message: str):
    # Get conversation history
    conversation_history = cl.user_session.get("conversation_history")

    # Add user message to history
    conversation_history.append({"role": "user", "content": message})

    # Generate response using OpenAI
    response = client.chat.completions.create(
        model="gpt-4",
        messages=conversation_history,
        max_tokens=150
    )

    # Extract assistant's reply
    reply = response.choices[0].message.content

    # Add assistant's reply to history
    conversation_history.append({"role": "assistant", "content": reply})

    # Update conversation history in session
    cl.user_session.set("conversation_history", conversation_history)

    # Send response back to user
    await cl.Message(content=reply).send()

if __name__ == "__main__":
    cl.run()
