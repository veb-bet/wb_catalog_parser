import pandas as pd
from parser.search_parser import get_products
from parser.product_parser import get_product_detail
from parser.seller_parser import get_seller_info

QUERY = "пальто из натуральной шерсти"


def main():
    products = get_products(QUERY, pages=2)

    full_data = []

    for item in products:
        detail = get_product_detail(item["nmId"])
        seller = get_seller_info(item["sellerId"])

        full_data.append({
            "Ссылка на товар": f"https://www.wildberries.ru/catalog/{item['nmId']}/detail.aspx",
            "Артикул": item["nmId"],
            "Название": detail.get("name"),
            "Цена": item["price"],
            "Описание": detail.get("description"),
            "Ссылки на изображения": detail.get("images"),
            "Характеристики": detail.get("characteristics"),
            "Название селлера": seller["seller_name"],
            "Ссылка на селлера": seller["seller_link"],
            "Размеры": item["sizes"],
            "Рейтинг": item["rating"],
            "Количество отзывов": item["reviews"],
            "Страна производства": detail.get("country")
        })

    df = pd.DataFrame(full_data)
    df.to_excel("data/full_catalog.xlsx", index=False)

    df_filtered = df[
        (df["Рейтинг"] >= 4.5) &
        (df["Цена"] <= 10000) &
        (df["Страна производства"] == "Россия")
    ]

    df_filtered.to_excel("data/filtered_catalog.xlsx", index=False)


if __name__ == "__main__":
    main()
