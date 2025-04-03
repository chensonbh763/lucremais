import requests
from flask import Flask, request

# Configurações
TOKEN = "7905605379:AAFyHj3AKMR2rQgh-z3jB4SyumNd0yKQ4zM"
INVITE_LINK = "https://t.me/+3WVbfyUHmrkyZDAx"
ADMIN_CHAT_ID = "@FelipeLucreMais"  # Pode ser @username ou o ID numérico

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json  # Recebe os dados da Cakto

    status = data.get("status")
    nome = data.get("customer_name", "Comprador")
    telegram_user = data.get("telegram_username")
    telefone = data.get("customer_phone")

    if status == "approved":
        # Enviar link de convite para o cliente
        mensagem_cliente = f"Olá {nome}! Sua compra foi aprovada. 🎉\n\nEntre no grupo exclusivo pelo link: {INVITE_LINK}"
        if telegram_user:
            enviar_mensagem(f"@{telegram_user}", mensagem_cliente)
        elif telefone:
            print(f"Não foi possível enviar para o número: {telefone}")
        
        # Notificar o admin
        msg_admin = f"✅ VENDA APROVADA\nNome: {nome}\nTelefone: {telefone}\nUsername: @{telegram_user}"
        enviar_mensagem(ADMIN_CHAT_ID, msg_admin)

    elif status == "refunded":
        msg_admin = f"⚠️ REEMBOLSO REALIZADO\nNome: {nome}\nTelefone: {telefone}\nUsername: @{telegram_user}"
        enviar_mensagem(ADMIN_CHAT_ID, msg_admin)

    return {"status": "ok"}

def enviar_mensagem(chat_id, mensagem):
    """Envia mensagem para um usuário do Telegram"""
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    params = {"chat_id": chat_id, "text": mensagem}
    response = requests.post(url, params=params)
    print(response.json())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
