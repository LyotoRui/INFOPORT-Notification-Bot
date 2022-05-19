import base64
import json
import re
from string import ascii_letters, digits


def loadDataFromSettings() -> dict:
    try:
        with open("settings.json", "r") as data_file:
            data = json.load(data_file)
            data_file.close()
        return data
    except FileNotFoundError:
        saveDataToSettings(
            {
                "WebLoginData": {"login": "", "password": ""},
                "RozetkaLoginData": {"login": "", "password": ""},
                "BotToken": "",
                "Users": {},
            }
        )
        loadDataFromSettings()


def checkDataForMistakes(data: dict) -> bool:
    for item in data.keys():
        if not len(data[item]):
            return False
    return True


def saveDataToSettings(data) -> None:
    with open("settings.json", "w") as data_file:
        json.dump(data, data_file)
    data_file.close()


def isNewPassportValid(password: str) -> bool:
    for letter in password:
        if letter not in ascii_letters + digits:
            return False
    return True


def isUserIdValid(id: str) -> bool:
    return id.isalnum()


def morphDataToNotify(
    source: str,
    order_id: str,
    customer_name: str,
    customer_phone: str,
    products: list,
    total_cost: str,
) -> str:
    return "\n".join(
        [
            f"{source}",
            "=============",
            f"Поступил заказ #{order_id}",
            "=============",
            f"Покупатель: {customer_name}",
            f"Телефон: {customer_phone}",
            "=============",
            "\n---------------------------\n".join(products),
            "=============",
            f"Итоговая сумма: {total_cost} грн",
        ]
    )


def passwordEncode(password) -> str:
    password_encode = str(password).encode("UTF-8")
    password = base64.b64encode(password_encode)
    return password.decode("UTF-8")


def exceptHtml(order: list) -> list:
    pattern = r"<[^>]*>"
    clear_list = [re.sub(pattern, "", str(item)) for item in order]
    clear_list[5] = ""
    return [item for item in clear_list if item != ""]
