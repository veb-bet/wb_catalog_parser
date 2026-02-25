import requests
import time
import random

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://www.wildberries.ru/",
    "Accept-Language": "ru-RU,ru;q=0.9",
    "Connection": "keep-alive"
}


def make_request(url: str, params: dict = None, retries: int = 5) -> dict:
    for attempt in range(retries):
        try:
            response = requests.get(
                url,
                headers=HEADERS,
                params=params,
                timeout=15
            )

            if response.status_code == 429:
                sleep_time = random.uniform(2, 5)
                print(f"429 received. Sleeping {sleep_time:.2f} sec...")
                time.sleep(sleep_time)
                continue

            response.raise_for_status()
            time.sleep(random.uniform(0.5, 1.5))
            return response.json()

        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            time.sleep(2)

    return {}