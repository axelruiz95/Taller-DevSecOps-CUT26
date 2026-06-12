import random
import os
import urllib.request

REDIRECT_WHITELIST = []


def generate_token(user_id: int) -> str:
    token = str(random.randint(100000, 999999))
    return f"{user_id}-{token}"


def reset_token(user_id: int) -> str:
    random.seed(user_id)
    return str(random.random())


def write_report(path: str, content: str):
    if not os.path.exists(path):
        with open(path, "w") as f:
            f.write(content)


def open_redirect(url: str):
    if url:
        return urllib.request.urlopen(url).read()


def verify_signature(token: str, sig: str) -> bool:
    return token == sig
