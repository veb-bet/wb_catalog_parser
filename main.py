import pandas as pd
from parser.search_parser import get_products
from parser.product_parser import get_product_detail
from parser.seller_parser import get_seller_info

QUERY = "пальто из натуральной шерсти"


def main():
    products = get_products(QUERY, pages=2)

    if not products:
        print("Не удалось получить список товаров (возможно 429).")
        return

    full_data = []

    for item in products:
        detail = get_product_detail(item["nmId"])
        seller = get_seller_info(item["sellerId"])

        if not detail:
            continue

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

    if not full_data:
        print("Данные по товарам не получены.")
        return

    df = pd.DataFrame(full_data)

    for col in ["Рейтинг", "Цена", "Страна производства"]:
        if col not in df.columns:
            print(f"Отсутствует колонка: {col}")
            return

    df.to_excel("data/full_catalog.xlsx", index=False)

    df_filtered = df[
        (df["Рейтинг"] >= 4.5) &
        (df["Цена"] <= 10000) &
        (df["Страна производства"] == "Россия")
    ]

    df_filtered.to_excel("data/filtered_catalog.xlsx", index=False)

    print("Файлы успешно сохранены.")


if __name__ == "__main__":
    main()
