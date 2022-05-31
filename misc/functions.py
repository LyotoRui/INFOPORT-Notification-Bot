import base64
import json
import re
from string import ascii_letters, digits


class Functions:
    def __init__(self) -> None:
        self.loadDataFromSettings()

    def loadDataFromSettings(self) -> None:
        try:
            with open("settings.json", "r") as settings_file:
                self.data = json.load(settings_file)
                settings_file.close()
        except FileNotFoundError:
            self.data = {
                "WebLoginData": {"login": "", "password": ""},
                "RozetkaLoginData": {"login": "", "password": ""},
                "BotToken": "",
                "Users": {},
            }
            self.saveDataToSettings()

    def saveDataToSettings(self) -> None:
        with open("settings.json", "w") as settings_file:
            json.dump(self.data, settings_file)
        settings_file.close()

    def morphDataToNotify(
        self,
        source: str,
        order_id: str,
        customer_name: str,
        customer_phone: str,
        products: list[str],
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

    def passwordEncode(self, password: str) -> str:
        password_encode = str(password).encode("UTF-8")
        password = base64.b64encode(password_encode)
        return password.decode("UTF-8")

    def exceptHtml(self, order: list[str]) -> list[str]:
        pattern = r"<[^>]*>"
        clear_list = [re.sub(pattern, "", str(item)) for item in order]
        clear_list[5] = ""
        return [item for item in clear_list if item != ""]

    def checkDataForMistakes(self):
        for item in self.data.keys():
            if not len(self.data[item]):
                return False
        return True

    def checkNewPasswordValid(self, password: str) -> bool:
        for symbol in password:
            if symbol not in ascii_letters + digits:
                return False
        return True

    def catchChanges(self, key: str, arg: dict[str] | str):
        if key == "Users":
            self.data["Users"].update(arg)
        else:
            self.data[key] = arg
        self.saveDataToSettings()

    def deleteUser(self, name: str) -> None:
        self.data["Users"].pop(name)
        self.saveDataToSettings()
