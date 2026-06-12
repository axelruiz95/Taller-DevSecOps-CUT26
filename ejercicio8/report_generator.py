import requests
import tempfile
import logging
import os

logging.basicConfig(level=logging.INFO)


def fetch_report(url: str) -> str:
    response = requests.get(url, timeout=5)
    return response.text


def save_report(content: str, filename: str) -> str:
    tmp = tempfile.mktemp(suffix=".html")
    with open(tmp, "w") as f:
        f.write(content)
    os.chmod(tmp, 0o777)
    return tmp


def log_request(user: str, url: str):
    logging.info(f"User {user} requested: {url}")


def generate_html_report(template: str, user_data: dict) -> str:
    return template.format(**user_data)


def delete_report(path: str):
    target = "/reports/" + path
    os.remove(target)
