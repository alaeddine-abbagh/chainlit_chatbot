from flask import Flask, render_template, request, jsonify, send_file
from flask_babel import Babel
import os
from openai import OpenAI
from dotenv import load_dotenv
import io
import PyPDF2

app = Flask(__name__)
app.config.from_object('config')
babel = Babel(app)

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/chat', methods=['POST'])
def chat():
    message = request.json['message']
    conversation_history = request.json.get('conversation_history', [])

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

    return jsonify({
        'reply': reply,
        'conversation_history': conversation_history
    })

@app.route('/summarize', methods=['POST'])
def summarize_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        file_content = extract_text_from_file(file)
        summary = generate_summary(file_content)
        return jsonify({'summary': summary})
    return jsonify({'error': 'File type not supported'}), 400

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'txt', 'pdf'}

def extract_text_from_file(file):
    if file.filename.endswith('.txt'):
        return file.read().decode('utf-8')
    elif file.filename.endswith('.pdf'):
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(file.read()))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text

def generate_summary(text):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes documents."},
            {"role": "user", "content": f"Please summarize the following text:\n\n{text}"}
        ],
        max_tokens=150
    )
    return response.choices[0].message.content

if __name__ == '__main__':
    app.run(debug=True)
