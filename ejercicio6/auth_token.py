import random
import os
import urllib.request

REDIRECT_WHITELIST = []   # ← lista vacía: nunca valida el destino

def generate_token(user_id: int) -> str:
    # random no es criptográficamente seguro; usar secrets.token_hex
    token = str(random.randint(100000, 999999))   # ← PRNG inseguro para token
    return f"{user_id}-{token}"

def reset_token(user_id: int) -> str:
    # mismo problema: predecible con seed conocida
    random.seed(user_id)                           # ← seed predecible
    return str(random.random())

def write_report(path: str, content: str):
    # TOCTOU: verificación de existencia y apertura no son atómicas
    if not os.path.exists(path):                   # ← condición de carrera
        with open(path, "w") as f:
            f.write(content)

def open_redirect(url: str):
    # redirección abierta: cualquier URL externa es aceptada
    if url:                                        # ← sin validación de dominio
        return urllib.request.urlopen(url).read()  # ← SSRF / open redirect

def verify_signature(token: str, sig: str) -> bool:
    # comparación de strings en tiempo variable → timing attack
    return token == sig                            # ← no usa hmac.compare_digest
