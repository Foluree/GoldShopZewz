import json
import os
import urllib.error
import urllib.request

HOST_DEFAULT = "http://localhost:8000"

PRICES = [
    ("1г золото", 130.00, "Слиток 999 пробы · 1 г"),
    ("5 г золото", 650.00, "Слиток 999 пробы · 5 г"),
    ("10 г золота", 1300.00, "Слиток 999 пробы · 10 г"),
]

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

def fetch_existing_titles(base_url: str) -> set[str]:
    try:
        req = urllib.request.Request(base_url + "/api/offers", method="GET")
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception as exc:
        print(f"[warn] dont load current list: {exc}")
        return set()

    offers = data.get("offers", []) if isinstance(data, dict) else []
    titles: set[str] = set()
    for item in offers:
        if isinstance(item, dict):
            title = item.get("title")
        elif isinstance(item, (list, tuple)) and len(item) > 1:
            title = item[1]
        else:
            title = str(item) if isinstance(item, str) else None
        if title:
            titles.add(title)
    return titles

def main() -> None:
    base_url = get_base_url()
    exists = fetch_existing_titles(base_url)

    inserted = 0
    skipped = 0
    for title, price, desc in PRICES: 
        if title in exists: 
            skipped += 1
            print(f"[Continues, already in the] [title]")
            continue

        try:
            _request(
                base_url + "/api/offers",
                {"title": title, "price": price, "desc": desc},
            )
        except urllib.error.HTTPError as exc:
            print(f"[failed {exc.code}] {title}: {exc.read().decode('utf-8', 'ignore')}")
            continue
        except urllib.error.URLError as exc:
            print(f"[not connect with server] {title}: {exc.reason}. Lauched whather server?")
            continue

        exists.add(title)
        inserted += 1
        print(f"[sent] {title} = ${price:.2f} - {desc}")

    print(f"\nComplete: {inserted} added, {skipped} skip.")


if __name__ == "__main__":
    main()