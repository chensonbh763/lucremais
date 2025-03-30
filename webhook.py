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

        if payment["status"] == "approved":
            user_id = payment["payer"]["email"]
            value = payment["transaction_amount"]
            print(f"✅ Pagamento aprovado para {user_id}, valor: R$ {value}")

            # Aqui você pode adicionar o saldo no bot

    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(port=5000, debug=True)
