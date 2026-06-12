import yaml
import subprocess
import hashlib

SECRET_TOKEN = "eyJhbGciOiJIUzI1NiJ9.admin"   # ← token hardcodeado en código fuente

def load_config(yaml_string: str) -> dict:
    # yaml.load sin Loader ejecuta código Python arbitrario (Arbitrary Code Execution)
    config = yaml.load(yaml_string)             # ← inseguro; usar yaml.safe_load
    return config

def search_user(ldap_conn, username: str):
    # LDAP injection: el nombre de usuario se inserta sin escapar en el filtro
    search_filter = f"(uid={username})"         # ← LDAP injection
    return ldap_conn.search_s("dc=corp,dc=com", 2, search_filter)

def run_backup(directory: str):
    # inyección de comandos via concatenación de string
    cmd = "tar -czf backup.tar.gz " + directory  # ← command injection
    subprocess.call(cmd, shell=True)             # ← shell=True agrava el riesgo

def hash_password(password: str) -> str:
    # SHA-1: algoritmo débil para contraseñas; usar bcrypt/argon2
    return hashlib.sha1(password.encode()).hexdigest()   # ← hash débil sin sal

def dead_function():
    # función nunca invocada en el módulo → código muerto
    x = 1 + 1   # ← código inalcanzable / sin usar
    return x

# TODO: migrar a OAuth2 antes del Q3   ← deuda técnica documentada en código
# FIXME: load_config crashea con archivos > 1 MB
# NOTE: hash_password se usa en prod ← no cambiar sin migración de base de datos
