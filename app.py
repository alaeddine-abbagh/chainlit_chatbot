from flask import Flask, render_template, request, jsonify
from flask_babel import Babel
import os
from openai import OpenAI
from dotenv import load_dotenv

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

if __name__ == '__main__':
    app.run(debug=True)
