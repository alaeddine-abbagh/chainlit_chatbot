from flask import Flask, render_template
from flask_babel import Babel

app = Flask(__name__)
app.config.from_object('config')
babel = Babel(app)

@app.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)
