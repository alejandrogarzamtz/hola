@app.route("/demo_ia_test", methods=["GET"])
def demo_ia_test():
    messages = [{"role": "user", "content": "¿Cuánto es 2 + 2?"}]
    stream = stream_text(messages)

    full_response = ""
    for line in stream:
        if line:
            try:
                data = json.loads(line)
                if "choices" in data:
                    delta = data["choices"][0].get("delta", {})
                    full_response += delta.get("content", "")
            except Exception as e:
                continue

    return jsonify({"respuesta": full_response.strip()})
