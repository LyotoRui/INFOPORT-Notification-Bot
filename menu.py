import os
import sys
from time import sleep

from pyfiglet import Figlet
from requests.exceptions import ConnectionError
from rich.console import Console
from urllib3.exceptions import MaxRetryError

from misc.bot import bot, notify
from misc.functions import Functions
from misc.rztk_checker import RZTKChecker
from misc.text_templates import *
from misc.web_checker import WebChecker

error = Console()


class Menu:
    def __init__(self) -> None:
        self.header = Figlet(font="slant").renderText("INFOPORT BOT")
        self.console = Console()
        self.main_menu = {0: self.__exit, 1: self.__doWork, 2: self._showSettingsMenu}
        self.settings_menu = {
            0: self._showMainMenu,
            1: self.__changeWebLogin,
            2: self.__changeRZTKLogin,
            3: self.__changeBotToken,
            4: self._showUserEditMenu,
        }
        self.user_menu = {
            0: self._showSettingsMenu,
            1: self.__addUser,
            2: self.__deleteUser,
        }
        self._showMainMenu()

    def __clear(self) -> None:
        os.system("cls")
        print(self.header)

    def __showError(self, error: str) -> None:
        self.__clear()
        self.console.print(error)
        sleep(1)

    def __exit(self) -> None:
        self.__clear()
        self.console.print(EXIT)
        sleep(1)
        sys.exit()

    def _showMainMenu(self) -> None:
        self.__clear()
        try:
            user_input = int(self.console.input(MAIN_MENU))
        except ValueError:
            self.__showError(WRONG_INPUT)
            self._showMainMenu()
        try:
            self.main_menu[user_input]()
        except KeyError:
            self.__showError(WRONG_INPUT)
            self._showMainMenu()

    def __doWork(self) -> None:
        self.__clear()
        if not Functions().checkDataForMistakes():
            self.__showError(SETTINGS_ERROR)
            self._showSettingsMenu()
        web = WebChecker()
        rztk = RZTKChecker()
        try:
            with self.console.status(WORKING, spinner="dots"):
                while True:
                    web.getNewOrders()
                    if len(web.new_orders):
                        for order in web.new_orders:
                            notify(order)
                    rztk.getNewOrders()
                    if len(rztk.new_orders):
                        for order in rztk.new_orders:
                            notify(order)
        except MaxRetryError and ConnectionError:
            self.__showError(NO_CONNECTION)
            self._showMainMenu()
        except KeyboardInterrupt:
            self.__showError(STOPING)
            self._showMainMenu()

    def _showSettingsMenu(self) -> None:
        self.__clear()
        try:
            user_input = int(self.console.input(SETTINGS_MENU))
        except ValueError:
            self.__showError(WRONG_INPUT)
            self._showSettingsMenu()
        try:
            self.settings_menu[user_input]()
        except KeyError:
            self.__showError(WRONG_INPUT)
            self._showSettingsMenu()

    def __changeWebLogin(self) -> None:
        self.__clear()
        new_login = self.console.input(LOGIN_CHANGE)
        if new_login == "0":
            self._showMainMenu()
        new_password = self.console.input(prompt=PASSWORD, password=True)
        if not Functions().checkNewPasswordValid(new_password):
            self.__showError(WRONG_PASSWORD)
            self.__changeWebLogin()
        Functions().catchChanges(
            key="WebLoginData", arg={"login": new_login, "password": new_password}
        )
        self.console.print(DONE)
        sleep(1)
        self._showSettingsMenu()

    def __changeRZTKLogin(self) -> None:
        self.__clear()
        new_login = self.console.input(LOGIN_CHANGE)
        if new_login == "0":
            self._showMainMenu()
        new_password = self.console.input(prompt=PASSWORD, password=True)
        if not Functions().checkNewPasswordValid(new_password):
            self.__showError(WRONG_PASSWORD)
            self.__changeWebLogin()
        Functions().catchChanges(
            key="RozetkaLoginData", arg={"login": new_login, "password": new_password}
        )
        self.console.print(DONE)
        sleep(1)
        self._showSettingsMenu()

    def __changeBotToken(self) -> None:
        self.__clear()
        new_token = self.console.input(TOKEN_CHANGE)
        Functions().catchChanges(key="BotToken", arg=new_token)
        bot.__init__(new_token)
        self.console.print(DONE)
        sleep(1)
        self._showSettingsMenu()

    def _showUserEditMenu(self) -> None:
        self.__clear()
        try:
            user_input = int(self.console.input(USER_EDIT_MENU))
        except ValueError:
            self.__showError(WRONG_INPUT)
            self._showUserEditMenu()
        try:
            self.user_menu[user_input]()
        except KeyError:
            self.__showError(WRONG_INPUT)
            self._showUserEditMenu()

    def __addUser(self) -> None:
        self.__clear()
        if not len(Functions().data["BotToken"]):
            self.__showError(NO_BOT_TOKEN)
            self._showSettingsMenu()
        self.console.print(USER_ADD_FAQ)
        try:
            bot.polling()
        except MaxRetryError and ConnectionError:
            self.__showError(NO_CONNECTION)
            self._showMainMenu()
        except KeyboardInterrupt:
            bot.stop_polling()
            self.__clear()
        user_id = self.console.input(USER_ID)
        if not user_id.isdigit():
            self.__showError(WRONG_INPUT)
            self.__addUser()
        user_name = self.console.input(USER_NAME)
        Functions().catchChanges(key="Users", arg={user_name: user_id})
        self.console.print(DONE)
        sleep(1)
        self._showSettingsMenu()

    def __deleteUser(self) -> None:
        self.__clear()
        for index, user in enumerate(Functions().data['Users'].keys()):
            self.console.print(f'{index + 1}. [bold]{user}[/bold]')
        user_input = self.console.input(USER_DELETE).capitalize()
        if user_input not in Functions().data['Users'].keys():
            self.__showError(USER_NOT_FOUND)
            self.__deleteUser()
        user_confirm = self.console.input(USER_DELETE_CONFIRMATION.replace('%', user_input))
        if user_confirm in 'Yy':
            Functions().deleteUser(name=user_input)
            self.console.print(DONE)
            sleep(1)
            self._showSettingsMenu()
        else:
            self._showSettingsMenu()



if __name__ == '__main__':
    try:
        Menu()
    except Exception as e:
        error.print_exception()
        input()
