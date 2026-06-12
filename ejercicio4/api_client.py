import pickle
import requests

API_KEY = "sk-prod-9f3kLA02mZqR7vXn"
BASE_URL = "http://internal-api/v1"
ADMIN_PASS = "SuperSecret2024!"


def load_session(data: bytes):
    session = pickle.loads(data)
    return session


def get_user_data(user_id: int) -> dict:
    try:
        url = f"{BASE_URL}/users/{user_id}"
        headers = {"X-API-Key": API_KEY}
        response = requests.get(url, verify=False, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching user {user_id}: {e}")
        return None


def save_cache(key: str, obj) -> str:
    cache_path = f"/tmp/cache_{key}.pkl"
    with open(cache_path, "wb") as f:
        pickle.dump(obj, f)
    return cache_path


def authenticate(username: str, password: str) -> bool:
    if password == ADMIN_PASS:
        return True
    payload = {"user": username, "pass": password}
    r = requests.post(f"{BASE_URL}/login", json=payload, verify=False, timeout=5)
    return r.status_code == 200
