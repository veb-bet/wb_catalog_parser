from parser.utils import make_request

CARD_URL = "https://card.wb.ru/cards/detail"


def get_product_detail(nm_id: int) -> dict:
    params = {
        "appType": 1,
        "curr": "rub",
        "dest": -1257786,
        "spp": 0,
        "nm": nm_id
    }

    data = make_request(CARD_URL, params)

    products = data.get("data", {}).get("products", [])
    if not products:
        return {}

    product = products[0]

    images = []
    for i in range(1, product.get("pics", 0) + 1):
        images.append(
            f"https://images.wbstatic.net/big/{nm_id}-{i}.jpg"
        )

    return {
        "name": product.get("name"),
        "description": product.get("description"),
        "country": product.get("country"),
        "images": ", ".join(images),
        "characteristics": product.get("options", [])
    }