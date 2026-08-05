"""
Автономный скрипт загрузки данных на сервер.

Отдельно от самой программы: запускается вручную командой
    python load_gold_price_1.py
и НЕ стартует вместе с приложением.

Данные отправляются не напрямую в БД, а через существующий HTTP-эндпоинт
POST /api/offers (определён в app/main_title_router.py), т.е. скрипт просто
подключается к работающему серверу и отправляет данные, которые заданы ниже.

Файл app/main_title_router.py не изменялся — он уже имеет нужную «ручку».
"""
import json
import os
import sys
import urllib.error
import urllib.request

# адрес работающего сервера (см. docker-compose: порт 8000 проброшен наружу)
HOST_DEFAULT = "http://localhost:8000"

# данные, которые нужно отправить на сервер
PRICES = [
    ("1г золота", 130.00, "Слиток 999 пробы · 1 г"),
    ("5г золота", 650.00, "Слиток 999 пробы · 5 г"),
    ("10г золота", 1300.00, "Слиток 999 пробы · 10 г"),
]


def get_base_url() -> str:
    """URL сервера берём из переменной окружения (опционально) или из дефолта."""
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
    """Узнаём, какие предложения уже есть, чтобы не плодить дубликаты.

    Старается распарсить ответ `/api/offers` максимально терпимо: элементы
    могут приходить как словари, так и как списки значений (строки таблицы).
    Если разобрать не удаётся или сервер отвечает не так, как ждали —
    просто возвращаем пустое множество и не мешаем загрузке.
    """
    try:
        req = urllib.request.Request(base_url + "/api/offers", method="GET")
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception as exc:
        print(f"[warn] не удалось получить текущий список: {exc}")
        return set()

    offers = data.get("offers", []) if isinstance(data, dict) else []
    titles: set[str] = set()
    for item in offers:
        if isinstance(item, dict):
            title = item.get("title")
        elif isinstance(item, (list, tuple)) and len(item) > 1:
            # строки вида [id, title, price, desc] — во 2-й ячейке title
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
            print(f"[пропущено, уже есть] {title}")
            continue

        try:
            _request(
                base_url + "/api/offers",
                {"title": title, "price": price, "desc": desc},
            )
        except urllib.error.HTTPError as exc:
            print(f"[ошибка {exc.code}] {title}: {exc.read().decode('utf-8', 'ignore')}")
            continue
        except urllib.error.URLError as exc:
            print(f"[нет связи с сервером] {title}: {exc.reason}. Запущен ли сервер?")
            continue

        exists.add(title)
        inserted += 1
        print(f"[отправлено] {title} = ${price:.2f} - {desc}")

    print(f"\nComplete: {inserted} added, {skipped} skip.")


if __name__ == "__main__":
    main()