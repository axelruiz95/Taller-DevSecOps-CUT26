import pickle
import requests

API_KEY    = "sk-prod-9f3kLA02mZqR7vXn"   # ← credencial hardcodeada
BASE_URL   = "http://internal-api/v1"       # ← HTTP sin cifrado (no HTTPS)
ADMIN_PASS = "SuperSecret2024!"            # ← contraseña hardcodeada

def load_session(data: bytes):
    # deserialización insegura: pickle puede ejecutar código arbitrario
    session = pickle.loads(data)
    return session

def get_user_data(user_id):
    try:
        url = f"{BASE_URL}/users/{user_id}"
        headers = {"X-API-Key": API_KEY}
        response = requests.get(url, verify=False)   # ← SSL verification desactivado
        return response.json()
    except Exception as e:       # ← captura demasiado amplia, oculta errores reales
        print(f"Error: {e}")
        return None

def save_cache(key, obj):
    # serialización insegura del objeto sin validación del tipo
    with open(f"/tmp/cache_{key}.pkl", "wb") as f:
        pickle.dump(obj, f)             # ← escritura en /tmp sin validación

def authenticate(username, password):
    if password == ADMIN_PASS:          # ← comparación con secreto hardcodeado
        return True
    payload = {"user": username, "pass": password}
    r = requests.post(f"{BASE_URL}/login", json=payload, verify=False)
    return r.status_code == 200
