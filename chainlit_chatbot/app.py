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
    files = None
 
    # Check if a file was uploaded
    if message.elements:
        for element in message.elements:
            if isinstance(element, cl.File):
                file = element
                print(file.mime)
                try:
                    if file.mime == "text/plain":
                        file_content = file.content.decode("utf-8") if file.content else ""
                    elif file.mime == "application/pdf":
                        # Debug: Print file size
                        print(f"PDF file size: {len(file.content) if file.content else 0} bytes")
                        
                        if not file.content:
                            await cl.Message(content="The uploaded PDF file appears to be empty.").send()
                            return
                        
                        pdf_content = file.content
                        pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_content))
                        
                        # Debug: Print number of pages
                        print(f"Number of pages in PDF: {len(pdf_reader.pages)}")
                        
                        file_content = ""
                        for page in pdf_reader.pages:
                            page_text = page.extract_text() or ""
                            file_content += page_text + "\n\n"
                            # Debug: Print length of extracted text for each page
                            print(f"Extracted text length for page: {len(page_text)} characters")
                        
                        # Check if extracted content is empty
                        if not file_content.strip():
                            await cl.Message(content="No text could be extracted from the PDF. It might be scanned or contain only images.").send()
                            return
                        
                        # Debug: Print total extracted text length
                        print(f"Total extracted text length: {len(file_content)} characters")
                    else:
                        await cl.Message(content=f"Unsupported file type: {file.mime}").send()
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
