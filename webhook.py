from flask import Flask, request, jsonify
import mercadopago

app = Flask(__name__)

# Credencial do Mercado Pago (vendedor)
ACCESS_TOKEN = "APP_USR-8823196038032226-030906-0c7a9b59dd2d7ae1ad5e5605e726ed1d-441758208"
sdk = mercadopago.SDK(ACCESS_TOKEN)

@app.route("/webhook", methods=["POST"])
def webhook():
    # Captura os dados recebidos pela requisição POST
    try:
        data = request.json
        
        if not data:
            return jsonify({"status": "error", "message": "Nenhum dado recebido"}), 400

        # Verifica se é a ação `payment.updated`
        if "action" in data and data["action"] == "payment.updated":
            payment_id = data.get("data", {}).get("id", None)
            
            if payment_id:
                # Obtém detalhes do pagamento via SDK do Mercado Pago
                payment_response = sdk.payment().get(payment_id)
                
                if payment_response["status"] == 200:
                    payment = payment_response["response"]
                    
                    # Extrai detalhes do pagamento
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

                    # Executa lógica adicional com base no status
                    if status == "approved":
                        print(f"🎉 Pagamento aprovado para {payer_email}, valor: R$ {value}")
                        # Aqui você pode adicionar saldo ao usuário no bot ou outras ações
                else:
                    print(f"⚠️ Erro ao consultar pagamento: {payment_response['status']}")
                    return jsonify({"status": "error", "message": "Erro ao consultar pagamento"}), payment_response["status"]
            else:
                return jsonify({"status": "error", "message": "ID do pagamento não encontrado"}), 400
        else:
            return jsonify({"status": "error", "message": "Ação desconhecida"}), 400
        
        return jsonify({"status": "success", "message": "Webhook processado"}), 200
    except Exception as e:
        print(f"❌ Erro ao processar webhook: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
