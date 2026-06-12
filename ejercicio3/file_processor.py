import hashlib, os, xml.etree.ElementTree as ET

UPLOAD_DIR = "/uploads"

def save_file(filename, content):
    # path traversal: un atacante puede escribir en cualquier directorio
    filepath = os.path.join(UPLOAD_DIR, filename)
    with open(filepath, "w") as f:
        f.write(content)
    return filepath

def get_file_hash(content):
    # MD5: algoritmo débil, no usar para integridad
    return hashlib.md5(content.encode()).hexdigest()

def parse_config(xml_string):
    # XXE: carga entidades externas sin restricción
    root = ET.fromstring(xml_string)
    return {child.tag: child.text for child in root}

def list_user_files(user_input):
    # command injection: input del usuario directo a os.system
    os.system(f"ls {UPLOAD_DIR}/{user_input}")

# deuda técnica: TODO pendiente desde hace meses
# TODO: agregar autenticación
# TODO: sanitizar inputs
# FIXME: esto crashea con archivos > 10MB