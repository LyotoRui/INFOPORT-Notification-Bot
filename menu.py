import sys
from pyfiglet import Figlet
from getpass import getuser, getpass
import os
import time
from web_checker import WebChecker
from rztk_checker import RZTKChecker
from misc_funcs import notify

web = WebChecker()
rztk = RZTKChecker()

class Menu:
    def __init__(self) -> None:
        os.system('cls')
        self._greet()
        self.main_menu = {
            1: self.startWorking,
            2: self._settings,
            3: self._exit
        }
        self.settings_menu = {
            1: self._webLoginChange,
            2: self._rozetkaLoginChange,
            3: self._userEdit,
            0: self._main
        }
        self.user_edit = {
            1: self.__addUser,
            2: self.__deleteUser,
            0: self._settings
        }
        self._main()

    def _greet(self):
        prev_text = Figlet(font="slant")
        print(prev_text.renderText("INFOPORT BOT"))

    def _main(self):
        try:
            user_input = int(
                input('\n'.join(
                    ['1. Запуск бота',
                    '2. Настройки',
                    '3. Выход',
                    '']
                    )
                )
            )
        except ValueError:
            self.__wrongInput()
            self._main()
        try:
            self.main_menu[user_input]()
        except KeyError:
            self.__wrongInput()
            self._main()

    def _clear(self):
        os.system('cls')
        self._greet()

    def __wrongInput(self):
        print('Неверный ввод')
        time.sleep(1)
        self._clear()

    def startWorking(self):
        print('Работаю... (Ctrl + C для завершения) ')
        try:
            while True:
                web.getNewOrders()
                if len(web.new_orders):
                    for order in web.new_orders:
                        notify(order)
                rztk.getNewOrders()
                if len(rztk.new_orders):
                    for order in rztk.new_orders:
                        notify(order)
        except KeyboardInterrupt:
            self._clear()
            print('Останавливаюсь...')
            time.sleep(1)
            self._clear()
            self._main()

    def _settings(self):
        try:
            user_input = int(
                input('\n'.join(
                    [
                        '1. Изменить данные входа на сайт',
                        '2. Изменить данные входа на Rozetka',
                        '3. Управление пользователями',
                        '0. Назад',
                        ''
                    ]
                    )
                )
            )
            self._clear()
        except ValueError:
            self.__wrongInput()
            self._settings()
        try:
            self.settings_menu[user_input]()
        except KeyError:
            print('Неверный ввод')
            time.sleep(1)
            self._clear()
            self._settings()

    def _webLoginChange(self):
        pass

    def _rozetkaLoginChange(self):
        pass

    def _userEdit(self):
        try:
            user_input = int(
                input(
                    '\n'.join(
                        [
                            '1. Добавить нового пользователя',
                            '2. Удалить пользователя',
                            '0. Назад',
                            ''
                        ]
                    )
                )
            )
        except ValueError:
            self.__wrongInput()
            self._userEdit()
        try:
            self.user_edit[user_input]()
        except KeyError:
            self.__wrongInput()
            self._userEdit()

    def __addUser(self):
        pass
    
    def __deleteUser(self):
        pass

    def _exit(self):
        print('Закрываемся...')
        time.sleep(1)
        sys.exit()

test = Menu()
