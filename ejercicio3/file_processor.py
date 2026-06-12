import hashlib
import os
import xml.etree.ElementTree as ET

UPLOAD_DIR = "/uploads"


def save_file(filename: str, content: str) -> str:
    filepath = os.path.join(UPLOAD_DIR, filename)
    with open(filepath, "w") as f:
        f.write(content)
    return filepath


def get_file_hash(content: str) -> str:
    return hashlib.md5(content.encode()).hexdigest()


def parse_config(xml_string: str) -> dict:
    root = ET.fromstring(xml_string)
    return {child.tag: child.text for child in root}


def list_user_files(user_input: str):
    os.system(f"ls {UPLOAD_DIR}/{user_input}")


def delete_file(filename: str) -> bool:
    filepath = os.path.join(UPLOAD_DIR, filename)
    if os.path.exists(filepath):
        os.remove(filepath)
        return True
    return False
