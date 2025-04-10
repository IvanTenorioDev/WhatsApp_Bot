import os
from flask import Flask, request, render_template
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from openai import OpenAI
from decouple import config
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Configuração das credenciais
TWILIO_ACCOUNT_SID = config('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = config('TWILIO_AUTH_TOKEN')
OPENAI_API_KEY = config('OPENAI_API_KEY')
TWILIO_PHONE_NUMBER = config('TWILIO_PHONE_NUMBER')

# Inicialização dos clientes
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
openai_client = OpenAI(api_key=OPENAI_API_KEY)

# Configuração do banco de dados
def init_db():
    conn = sqlite3.connect('messages.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS messages
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
         phone TEXT,
         message TEXT,
         response TEXT,
         timestamp DATETIME,
         credits_used INTEGER)
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS credits
        (phone TEXT PRIMARY KEY,
         amount INTEGER)
    ''')
    conn.commit()
    conn.close()

init_db()

def get_user_credits(phone):
    conn = sqlite3.connect('messages.db')
    c = conn.cursor()
    c.execute('SELECT amount FROM credits WHERE phone = ?', (phone,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else 1000  # Créditos iniciais gratuitos

def update_user_credits(phone, amount):
    conn = sqlite3.connect('messages.db')
    c = conn.cursor()
    c.execute('INSERT OR REPLACE INTO credits (phone, amount) VALUES (?, ?)',
              (phone, amount))
    conn.commit()
    conn.close()

def save_message(phone, message, response):
    conn = sqlite3.connect('messages.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO messages (phone, message, response, timestamp, credits_used)
        VALUES (?, ?, ?, ?, ?)
    ''', (phone, message, response, datetime.now(), 1))
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/webhook', methods=['POST'])
def webhook():
    incoming_msg = request.values.get('Body', '').lower()
    sender = request.values.get('From', '')
    
    # Verificar créditos
    credits = get_user_credits(sender)
    if credits <= 0:
        response = MessagingResponse()
        response.message("Você não tem mais créditos. Acesse nossa página para comprar mais: https://seu-site.com")
        return str(response)
    
    # Gerar resposta com GPT-3.5
    try:
        chat_completion = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um assistente prestativo e amigável."},
                {"role": "user", "content": incoming_msg}
            ]
        )
        ai_response = chat_completion.choices[0].message.content
        
        # Atualizar créditos e salvar mensagem
        update_user_credits(sender, credits - 1)
        save_message(sender, incoming_msg, ai_response)
        
        # Enviar resposta
        response = MessagingResponse()
        response.message(ai_response)
        return str(response)
        
    except Exception as e:
        response = MessagingResponse()
        response.message("Desculpe, ocorreu um erro. Tente novamente mais tarde.")
        return str(response)

if __name__ == '__main__':
    app.run(debug=True, port=5001) 