from flask import Flask, render_template, request, jsonify, session
from contexts import get_contextual_prompt
from personalities import get_personality_style
from flask_session import Session
import openai
import sqlite3
import uuid

def init_db():
    conn = sqlite3.connect('chatlog.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS customer_service_chatlog (session_id TEXT, user_message TEXT, bot_message TEXT)''')
    # c.execute('''CREATE TABLE IF NOT EXISTS product_description_chatlog (session_id TEXT, user_message TEXT, bot_message TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS customer_service_prompts_log (session_id TEXT, prompt TEXT)''')
    # c.execute('''CREATE TABLE IF NOT EXISTS product_description_prompts_log (session_id TEXT, prompt TEXT)''')
    c.execute('DELETE FROM customer_service_chatlog')
    # c.execute('DELETE FROM product_description_chatlog')
    c.execute('DELETE FROM customer_service_prompts_log')
    # c.execute('DELETE FROM product_description_prompts_log')
    conn.commit()
    conn.close()


init_db()
app = Flask(__name__)
openai.api_key = "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"
# Secret key for session management
app.config['SECRET_KEY'] = '40524b102b7aff5d1a8e86544a0de61d'
# Configure session to use filesystem (instead of signed cookies)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
# Initialize the session
Session(app)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/customer_service')
def customer_service():
    # Ensure a unique session for this service
    if 'customer_service_session_id' not in session:
        session['customer_service_session_id'] = str(uuid.uuid4())
    return render_template('customer_service.html', session_id=session['customer_service_session_id'])


@app.route('/customer_service_chat', methods=['POST'])
def chat():
    data = request.json
    service_type = data.get('service_type')  # Add a parameter to identify the service
    user_message = data['message']
    selected_context = data.get('context', '')
    selected_personality = data.get('personality', '')
    selected_language = data.get('language', 'English')

    # Construct the prompt with context and personality
    personality_prompt = get_personality_style(selected_personality, user_message)
    contextual_prompt = get_contextual_prompt(selected_context, personality_prompt)
    prompt_template = f"Please ignore all previous instructions. Respond only in {selected_language} language. {contextual_prompt}."

    conn = sqlite3.connect('chatlog.db')
    c = conn.cursor()
    prompt_table_name = "customer_service_prompts_log"
    session_id = session.get(f'{service_type}_session_id')
    table_name = "customer_service_chatlog"

    # Insert custom prompt created based on user query
    c.execute(f"INSERT INTO {prompt_table_name} (session_id, prompt) VALUES (?, ?)", (session_id, prompt_template))
    conn.commit()

    model_engine = "text-davinci-002"
    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt_template,
        max_tokens=250 # tokens
    )
    bot_message = response.choices[0].text.strip()
    
    # Insert user query and bot response
    c.execute(f"INSERT INTO {table_name} (session_id, user_message, bot_message) VALUES (?, ?, ?)",
              (session_id, user_message, bot_message))
    conn.commit()
    conn.close()

    return jsonify({'message': bot_message, 'prompt': prompt_template})


@app.route('/customer_service_export-chat/<service_type>')
def export_chat(service_type):
    session_key = f'{service_type}_session_id'
    session_id = session.get(session_key)
    conn = sqlite3.connect('chatlog.db')
    cursor = conn.cursor()

    table_name = "customer_service_chatlog"
    query = f"SELECT user_message, bot_message FROM {table_name} WHERE session_id = ?"
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

@app.route('/customer_service_export-prompts/<service_type>')
def export_prompts(service_type):
    session_key = f'{service_type}_session_id'
    session_id = session.get(session_key)
    conn = sqlite3.connect('chatlog.db')
    cursor = conn.cursor()

    # Assuming you have a table or a way to store prompts
    table_name = "customer_service_prompts_log"
    query = f"SELECT prompt FROM {table_name} WHERE session_id = ?"
    cursor.execute(query, (session_id,))
    prompt_data = cursor.fetchall()

    if not prompt_data:
        return "No prompt data available for this session.", 404

    # Convert prompt data to TXT format
    txt_data = "\n\n".join([f"Prompt: {row[0]}" for row in prompt_data])

    conn.close()

    # Set headers for file download
    headers = {
        'Content-Disposition': 'attachment; filename=prompt_history.txt',
        'Content-Type': 'text/plain'
    }

    return txt_data, 200, headers

