import requests
import base64
import json

API_URL = ""
HEADERS = {"Authorization": "Bearer "}

def detectar_personas(imagen_path):
    with open(imagen_path, "rb") as f:
        img_bytes = f.read()
    data = {
        "inputs": base64.b64encode(img_bytes).decode("utf-8")
    }
    response = requests.post(API_URL, headers=HEADERS, json=data)
    response.raise_for_status()
    results = response.json()
    for obj in results:
        if obj.get("label") == "person" and obj.get("score", 0) > 0.7:
            print(f"🚨 Persona detectada en: {imagen_path}")
            return True
    print(f"✅ Sin personas en: {imagen_path}")
    return False

# probar en una imagen
detectar_personas("/home/dahuaftp/dahua/gallinas/2025-07-25/20-22-19.jpg")
