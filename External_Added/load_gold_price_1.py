import urllib.error
from additaonal_funtianal_load import fetch_existing_titles, get_base_url, _request

PRICES = [
    ("1г золото", 130.00, "Слиток 999 пробы · 1 г"),
    ("5 г золото", 650.00, "Слиток 999 пробы · 5 г"),
    ("10 г золота", 1300.00, "Слиток 999 пробы · 10 г"),
]
    
def main_price() -> None:
    base_url = get_base_url()
    exists = fetch_existing_titles(base_url, "/api/offers", "offers", "title")

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
    main_price()