import os
import json
import chainlit as cl
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ensure_serializable(obj):
    """Ensure the object is JSON serializable."""
    if isinstance(obj, dict):
        return {k: ensure_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [ensure_serializable(item) for item in obj]
    elif hasattr(obj, 'model_dump'):
        # This handles pydantic models, including OpenAI's Message object
        return ensure_serializable(obj.model_dump())
    elif hasattr(obj, '__dict__'):
        return ensure_serializable(obj.__dict__)
    else:
        try:
            json.dumps(obj)
            return obj
        except (TypeError, OverflowError):
            return str(obj)

@cl.on_chat_start
async def start():
    cl.user_session.set("conversation_history", [])

@cl.on_message
async def main(message: str):
    # Get conversation history
    conversation_history = cl.user_session.get("conversation_history")

    # Add user message to history
    conversation_history.append({"role": "user", "content": message})

    try:
        # Generate response using OpenAI
        response = client.chat.completions.create(
            model="gpt-4",
            messages=conversation_history,
            max_tokens=150
        )

        # Extract assistant's reply
        assistant_message = response.choices[0].message
        reply = assistant_message.content

        # Add assistant's reply to history
        conversation_history.append(ensure_serializable(assistant_message))

        # Update conversation history in session
        cl.user_session.set("conversation_history", conversation_history)

        # Send response back to user
        await cl.Message(content=reply).send()
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        await cl.Message(content=error_message).send()

if __name__ == "__main__":
    cl.run()
