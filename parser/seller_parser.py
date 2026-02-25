def get_seller_info(seller_id: int) -> dict:
    return {
        "seller_name": f"Seller {seller_id}",
        "seller_link": f"https://www.wildberries.ru/seller/{seller_id}"
    }