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
    print(f"Ensuring serializable for object of type: {type(obj)}")
    if isinstance(obj, dict):
        print("Object is a dictionary")
        return {k: ensure_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        print("Object is a list or tuple")
        return [ensure_serializable(item) for item in obj]
    elif hasattr(obj, 'model_dump'):
        print("Object has model_dump method")
        return ensure_serializable(obj.model_dump())
    elif hasattr(obj, '__dict__'):
        print("Object has __dict__ attribute")
        return ensure_serializable(obj.__dict__)
    else:
        try:
            json.dumps(obj)
            print("Object is already JSON serializable")
            return obj
        except (TypeError, OverflowError) as e:
            print(f"Object is not JSON serializable: {e}")
            return str(obj)

@cl.on_chat_start
async def start():
    cl.user_session.set("conversation_history", [])

@cl.on_message
async def main(message: str):
    print("Received message:", message)
    # Get conversation history
    conversation_history = cl.user_session.get("conversation_history")
    print("Current conversation history:", conversation_history)

    # Add user message to history
    conversation_history.append({"role": "user", "content": message})

    try:
        # Generate response using OpenAI
        print("Generating response using OpenAI")
        response = client.chat.completions.create(
            model="gpt-4",
            messages=conversation_history,
            max_tokens=150
        )

        # Extract assistant's reply
        assistant_message = response.choices[0].message
        reply = assistant_message.content
        print("Assistant's reply:", reply)

        print("Ensuring assistant's message is serializable")
        serializable_message = ensure_serializable(assistant_message)
        print("Serializable message:", serializable_message)

        # Add assistant's reply to history
        conversation_history.append(serializable_message)

        # Update conversation history in session
        print("Updating conversation history in session")
        cl.user_session.set("conversation_history", conversation_history)

        # Send response back to user
        print("Sending response back to user")
        await cl.Message(content=reply).send()
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        error_message = f"An error occurred: {str(e)}"
        await cl.Message(content=error_message).send()

if __name__ == "__main__":
    cl.run()
