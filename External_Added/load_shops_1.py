import urllib.error
from External_Added.additaonal_funtianal_load import fetch_existing_titles, get_base_url, _request

SHOPS = [
    ("Санлайт", "ТЦ «Атриум», Земляной Вал, д. 33, Москва", "10:00–22:00", "+7 495 000-11-01"),
    ("Адамас", "ТЦ «Европейский», пл. Киевского Вокзала, д. 2, Москва", "10:00–22:00", "+7 495 000-11-02"),
    ("SOKOLOV", "ГУМ, Красная площадь, д. 3, Москва", "10:00–22:00", "+7 495 000-11-03"),
    ("585 Золотой", "ТЦ «Охотный Ряд», Манежная площадь, д. 1, Москва", "10:00–22:00", "+7 495 000-11-04"),
    ("Pandora", "ТЦ «Цветной», Цветной бульвар, д. 15, Москва", "10:00–22:00", "+7 495 000-11-05"),
]


def main_shops() -> None:
    base_url = get_base_url()
    exists = fetch_existing_titles(base_url, "/api/shops", "shops", "name")

    inserted = 0
    skipped = 0
    for name, address, hours, phone in SHOPS:
        if name in exists:
            skipped += 1
            print(f"[Continues, already in the] [name]")
            continue

        try:
            _request(
                base_url + "/api/shops",
                {"name": name, "address": address, "hours": hours, "phone": phone},
            )
        except urllib.error.HTTPError as exc:
            print(f"[failed {exc.code}] {name}: {exc.read().decode('utf-8', 'ignore')}")
            continue
        except urllib.error.URLError as exc:
            print(f"[not connect with server] {name}: {exc.reason}. Lauched whather server?")
            continue

        exists.add(name)
        inserted += 1
        print(f"[sent] {name} - {address} | {hours} | {phone}")

    print(f"\nComplete: {inserted} added, {skipped} skip.")


if __name__ == "__main__":
    main_shops()