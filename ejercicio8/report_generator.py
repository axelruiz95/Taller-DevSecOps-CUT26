import requests
import tempfile
import logging
import os

logging.basicConfig(level=logging.INFO)

def fetch_report(url: str) -> str:
    # SSRF: el servidor realiza peticiones a URLs controladas por el usuario
    response = requests.get(url, timeout=5)   # ← sin validación del destino
    return response.text

def save_report(content: str, filename: str) -> str:
    # archivo temporal predecible y sin permisos restrictivos
    tmp = tempfile.mktemp(suffix=".html")     # ← mktemp es inseguro (TOCTOU)
    with open(tmp, "w") as f:
        f.write(content)
    os.chmod(tmp, 0o777)                       # ← permisos excesivos
    return tmp

def log_request(user: str, url: str):
    # log injection: el input del usuario llega sin escapar al log
    logging.info(f"User {user} requested: {url}")   # ← log injection

def generate_html_report(template: str, user_data: dict) -> str:
    # format string con datos de usuario → posible inyección en plantilla
    return template.format(**user_data)        # ← template injection

def delete_report(path: str):
    # path traversal en eliminación
    target = "/reports/" + path               # ← sin normalización de ruta
    os.remove(target)
