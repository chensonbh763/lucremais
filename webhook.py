import os
import requests
from flask import Flask, request

# Configurações
TOKEN = "7905605379:AAFyHj3AKMR2rQgh-z3jB4SyumNd0yKQ4zM"
INVITE_LINK = "https://t.me/+3WVbfyUHmrkyZDAx"

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json  # Recebe os dados da Cakto

    if data.get("status") == "approved":
        nome = data.get("customer_name", "Comprador")
        telefone = data.get("customer_phone")
        telegram_user = data.get("telegram_username")  # Se tiver username do Telegram

        mensagem = f"Olá {nome}! Sua compra foi aprovada. 🎉\n\nEntre no grupo exclusivo pelo link: {INVITE_LINK}"

        if telegram_user:
            enviar_mensagem(f"@{telegram_user}", mensagem)
        elif telefone:
            enviar_mensagem_por_numero(telefone, mensagem)
        else:
            print("Nenhum contato do cliente disponível.")

    return {"status": "ok"}

def enviar_mensagem(chat_id, mensagem):
    """Envia mensagem para um usuário do Telegram"""
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    params = {"chat_id": chat_id, "text": mensagem}
    response = requests.post(url, params=params)
    print(response.json())

def enviar_mensagem_por_numero(numero, mensagem):
    """Tenta enviar mensagem pelo número de telefone"""
    # O Telegram não suporta envio por número diretamente, então essa função pode ser adaptada
    print(f"Mensagem para {numero}: {mensagem}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
