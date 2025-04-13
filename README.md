# WhatsApp AI Bot

Um bot de WhatsApp que utiliza GPT-3.5 para responder mensagens, com integração Twilio e armazenamento em SQLite.

**Projeto em desenvolvimento**

## Funcionalidades

- Recebe e responde mensagens do WhatsApp via Twilio
- Processa respostas usando GPT-3.5 da OpenAI
- Armazena histórico de conversas em SQLite
- Sistema de créditos por usuário (1000 mensagens = R$ 10)
- Interface web simples para instruções e compra de créditos

## Tecnologias

- Python 3.9+
- Flask 3.0.2
- OpenAI API (GPT-3.5 Turbo)
- Twilio WhatsApp API
- SQLite
- Railway (Deploy)

## Pré-requisitos

1. Conta na Twilio (gratuita)
2. Conta na OpenAI
3. Conta no Railway (opcional, para deploy)

## Configuração

### 1. Configuração do Twilio

1. Acesse [Twilio Console](https://console.twilio.com)
2. Crie uma conta gratuita
3. No console, vá para "Messaging" > "Try it Out" > "Send a WhatsApp Message"
4. Siga as instruções para ativar o sandbox do WhatsApp
5. Anote seu:
   - Account SID
   - Auth Token
   - Número do WhatsApp Twilio

### 2. Configuração da OpenAI

1. Acesse [OpenAI Platform](https://platform.openai.com)
2. Crie uma conta ou faça login
3. Vá para "API Keys"
4. Crie uma nova API key
5. Anote sua API key

### 3. Configuração Local

1. Clone este repositório
2. Crie um arquivo `.env` na raiz do projeto com:
```env
TWILIO_ACCOUNT_SID=seu_sid
TWILIO_AUTH_TOKEN=seu_token
OPENAI_API_KEY=sua_api_key
TWILIO_PHONE_NUMBER=seu_numero_twilio
```
3. Instale as dependências:
```bash
pip install -r requirements.txt
```
4. Execute o servidor:
```bash
python app.py
```

### 4. Deploy no Railway

1. Clique no botão abaixo para fazer deploy no Railway:

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template?template=https://github.com/seu-usuario/whatsapp-bot)

2. Configure as variáveis de ambiente no Railway:
   - TWILIO_ACCOUNT_SID
   - TWILIO_AUTH_TOKEN
   - OPENAI_API_KEY
   - TWILIO_PHONE_NUMBER

3. Após o deploy, copie a URL do seu app no Railway
4. Configure esta URL no Twilio Console:
   - Vá para "Messaging" > "Settings" > "WhatsApp Sandbox Settings"
   - Cole sua URL + "/webhook" no campo "When a message comes in"

## Uso

1. Envie uma mensagem para o número do WhatsApp fornecido pelo Twilio
2. O bot responderá usando GPT-3.5
3. Para comprar créditos, acesse a página inicial do bot

## Créditos

- 1000 mensagens = R$ 10
- Pagamento via link na página inicial
- Histórico de conversas armazenado localmente

## Suporte

Para suporte, abra uma issue neste repositório. 