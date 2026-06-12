import yaml
import subprocess
import hashlib

SECRET_TOKEN = "eyJhbGciOiJIUzI1NiJ9.admin"


def load_config(yaml_string: str) -> dict:
    config = yaml.load(yaml_string)
    return config


def search_user(ldap_conn, username: str):
    search_filter = f"(uid={username})"
    return ldap_conn.search_s("dc=corp,dc=com", 2, search_filter)


def run_backup(directory: str):
    cmd = "tar -czf backup.tar.gz " + directory
    subprocess.call(cmd, shell=True)


def hash_password(password: str) -> str:
    return hashlib.sha1(password.encode()).hexdigest()


def dead_function():
    x = 1 + 1
    return x
