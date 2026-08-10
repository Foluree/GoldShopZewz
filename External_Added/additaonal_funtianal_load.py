import urllib.request
import json
import os

HOST_DEFAULT = "http://localhost:8000"

def get_base_url() -> str:
    return os.environ.get("SRV_BASE_URL", HOST_DEFAULT).rstrip("/")

def _request(url: str, payload: dict | None = None) -> dict:
    data = None
    headers = {}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=20) as resp:
        body = resp.read().decode("utf-8")
        return json.loads(body) if body else {}

def fetch_existing_titles(base_url: str, url_name, get_name, get_ti) -> set[str]:
    try:
        req = urllib.request.Request(base_url + url_name, method="GET")
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception as exc:
        print(f"[warn] dont load current list: {exc}")
        return set()

    offers = data.get(get_name, []) if isinstance(data, dict) else []
    titles: set[str] = set()
    for item in offers:
        if isinstance(item, dict):
            title = item.get(get_ti)
        elif isinstance(item, (list, tuple)) and len(item) > 1:
            title = item[1]
        else:
            title = str(item) if isinstance(item, str) else None
        if title:
            titles.add(title)
    return titles