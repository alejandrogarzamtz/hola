import requests
import json

url = "http://127.0.0.1:5000/api/chat"  # asegúrate que sea la correcta

# Mensaje de prueba
mensaje = [
    {"role": "user", "content": "Say hello in English."}
]

try:
    response = requests.post(url, data={
        "messages": json.dumps(mensaje),
        "model-selection": "Default Model"
    }, stream=True)

    print("🔄 Esperando respuesta de la IA...")

    full_response = ""
    for line in response.iter_lines():
        if line:
            data = json.loads(line.decode("utf-8"))
            if "choices" in data and data["choices"]:
                delta = data["choices"][0].get("delta", {})
                full_response += delta.get("content", "")

    print("✅ Respuesta recibida:")
    print(full_response)

except Exception as e:
    print("❌ Error al llamar a la API:")
    print(e)
