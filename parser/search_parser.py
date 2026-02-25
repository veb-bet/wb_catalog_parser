from parser.utils import make_request

SEARCH_URL = "https://search.wb.ru/exactmatch/ru/common/v4/search"


def get_products(query: str, pages: int = 1) -> list:
    products = []

    for page in range(1, pages + 1):
        params = {
            "query": query,
            "page": page,
            "resultset": "catalog",
            "appType": 1,
            "curr": "rub",
            "dest": -1257786,
            "regions": 80,
            "sort": "popular",
            "spp": 0
        }

        data = make_request(SEARCH_URL, params)

        if "data" not in data:
            continue

        for item in data["data"]["products"]:
            products.append({
                "nmId": item["id"],
                "price": item.get("salePriceU", 0) / 100,
                "rating": item.get("rating", 0),
                "reviews": item.get("feedbacks", 0),
                "sellerId": item.get("supplierId"),
                "sizes": ", ".join(
                    [s["name"] for s in item.get("sizes", [])]
                )
            })

    return products