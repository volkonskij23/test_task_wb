import requests
import pandas as pd


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0",
    "Accept": "*/*",
    "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
    "Origin": "https://www.wildberries.ru",
    "Connection": "keep-alive",
    "Referer": "https://www.wildberries.ru/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "cross-site",
    "If-Modified-Since": "Tue, 07 Nov 2023 18:15:50 GMT",
}


# Код страны: ru, by, kz, kg, am, uz, az
country              = "ru"

# Юрл с информацией о пунктах выдачи
target_url           = "https://static-basket-01.wb.ru/vol0/data/all-poo-fr-v8.json"

# Тип точки.
delivery_point_types = {0: "Постамат", 3: "Пункт выдачи", 4: "Пункт выдачи"}

# Датафрейм для записи в ексель
df_list              = []
col_names            = ["Широта", "Долгота", "Адрес", "Тип пункта"]

try:
    response = requests.get(target_url, headers=headers)

    if response.status_code != 200:
        print("Ошибка:{}".format(response.status_code))
    else:
        all_delivery_points    = response.json()
        county_delivery_points = {}

        # Получение пунктов выдачи в зависимости от выбранной страны
        for country_info in all_delivery_points:
            if country == country_info["country"]:

                county_delivery_points = country_info["items"]
                break

        for delivery_point_info in county_delivery_points:

            latitude            = delivery_point_info["coordinates"][0]
            longitude           = delivery_point_info["coordinates"][1]
            address             = delivery_point_info["address"]
            delivery_point_type = ""

            # Тип пункта
            if "pickupType" in delivery_point_info.keys():
                delivery_point_type = delivery_point_types[
                    delivery_point_info["pickupType"]
                ]
            elif "emp" in delivery_point_info.keys():
                delivery_point_type = "Склад WB"
            elif "isHkn" in delivery_point_info.keys():
                delivery_point_type = "Склад WB"
            else:
                delivery_point_type = "Сортировочный центр WB"

            df_list.append([latitude, longitude, address, delivery_point_type])

        df = pd.DataFrame(
            df_list,
            columns=col_names,
        )
        df.to_excel(r"result.xlsx", index=False)

except Exception as e:

    print("Ошибка: {}".format(e))
