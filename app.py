from flask import Flask, render_template, request, jsonify, session
from flask_session import Session
import openai
import sqlite3
import uuid


def init_db():
    conn = sqlite3.connect('chatlog.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS chatlog (session_id TEXT, user_message TEXT, bot_message TEXT)''')
    c.execute('DELETE FROM chatlog')
    conn.commit()
    conn.close()


init_db()
app = Flask(__name__)
openai.api_key = "your-api-key"
# Secret key for session management
app.config['SECRET_KEY'] = 'your-secret-key'
# Configure session to use filesystem (instead of signed cookies)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
# Initialize the session
Session(app)


@app.route('/')
def index():
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())  # method to generate a unique ID
        # Add a print statement to debug
        print("Session ID:", session['session_id'])
    return render_template('index.html', session_id=session['session_id'])


@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json['message']
    model_engine = "text-davinci-002"
    response = openai.Completion.create(
        engine=model_engine,
        prompt=user_message,
        max_tokens=250 # tokens
    )
    bot_message = response.choices[0].text.strip()

    # Log to database
    conn = sqlite3.connect('chatlog.db')
    c = conn.cursor()
    session_id = session.sid
    c.execute("INSERT INTO chatlog (session_id, user_message, bot_message) VALUES (?, ?, ?)",
              (session_id, user_message, bot_message))
    conn.commit()
    conn.close()

    return jsonify({'message': bot_message})


@app.route('/export-chat')
def export_chat():
    session_id = session.sid
    conn = sqlite3.connect('chatlog.db')
    cursor = conn.cursor()

    query = "SELECT user_message, bot_message FROM chatlog WHERE session_id = ?"
    cursor.execute(query, (session_id,))
    chat_data = cursor.fetchall()

    if not chat_data:
        print("No chat data found for session:", session_id)
        return "No chat data available for this session.", 404

    # Convert chat data to TXT format
    txt_data = ""
    for row in chat_data:
        txt_data += f'User: {row[0]}\nBot: {row[1]}\n\n'

    conn.close()

    # Set headers for file download
    headers = {
        'Content-Disposition': 'attachment; filename=chat_history.txt',
        'Content-Type': 'text/plain'
    }

    return txt_data, 200, headers

