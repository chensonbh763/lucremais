from flask import Flask, request, jsonify
import mercadopago

app = Flask(__name__)

ACCESS_TOKEN = "APP_USR-8823196038032226-030906-0c7a9b59dd2d7ae1ad5e5605e726ed1d-441758208"
sdk = mercadopago.SDK(ACCESS_TOKEN)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json

    if "action" in data and data["action"] == "payment.updated":
        payment_id = data["data"]["id"]
        payment = sdk.payment().get(payment_id)["response"]

        status = payment.get("status", "desconhecido")
        value = payment.get("transaction_amount", 0.0)
        payer_email = payment["payer"].get("email", "desconhecido")
        payment_method = payment.get("payment_method_id", "desconhecido")

        print(f"🔔 Webhook recebido!")
        print(f"🆔 ID do Pagamento: {payment_id}")
        print(f"💰 Valor: R$ {value}")
        print(f"📧 Pagador: {payer_email}")
        print(f"💳 Método de Pagamento: {payment_method}")
        print(f"✅ Status: {status}")

        if status == "approved":
            print(f"🎉 Pagamento aprovado para {payer_email}, valor: R$ {value}")
            # Aqui você pode adicionar saldo ao usuário no bot

    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
