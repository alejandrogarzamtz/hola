@app.route('/api/test-chat', methods=['GET'])
def test_api_ai_gateway():
    import json
    import requests

    url = "http://127.0.0.1:5000/api/chat"  # asegúrate que sea la correcta

    mensaje = [
        {"role": "user", "content": "De donde viene el nombre alejandro? respuesta super corta."}
    ]

    try:
        response = requests.post(url, data={
            "messages": json.dumps(mensaje),
            "model-selection": "Default Model"
        }, stream=True)

        full_response = ""
        for line in response.iter_lines():
            if line:
                data = json.loads(line.decode("utf-8"))
                if "choices" in data and data["choices"]:
                    delta = data["choices"][0].get("delta", {})
                    full_response += delta.get("content", "")

        return jsonify({"respuesta": full_response}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
