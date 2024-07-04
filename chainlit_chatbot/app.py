import os
import chainlit as cl
from openai import OpenAI
from dotenv import load_dotenv
import pdfplumber
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
    files = None
 
    # Check if a file was uploaded
    if message.elements:
        for element in message.elements:
            if isinstance(element, cl.File):
                file = element
                print(f"File MIME type: {file.mime}")
                print(f"File size: {len(file.content)} bytes")
                
                try:
                    if file.mime == "application/pdf":
                        if not file.content:
                            await cl.Message(content="The uploaded PDF file appears to be empty.").send()
                            return
                        
                        file_content = ""
                        try:
                            with pdfplumber.open(io.BytesIO(file.content)) as pdf:
                                print(f"Number of pages in PDF: {len(pdf.pages)}")
                                for i, page in enumerate(pdf.pages):
                                    page_text = page.extract_text() or ""
                                    file_content += page_text + "\n\n"
                                    print(f"Page {i+1} extracted text length: {len(page_text)} characters")
                        except Exception as e:
                            await cl.Message(content=f"An error occurred while processing the PDF: {str(e)}").send()
                            return
                        
                        if not file_content.strip():
                            await cl.Message(content="No text could be extracted from the PDF. It might be scanned or contain only images.").send()
                            return
                        
                        print(f"Total extracted text length: {len(file_content)} characters")
                        
                        # Summarize file content
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
