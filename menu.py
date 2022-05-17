import os
import sys
import time
from getpass import getpass

from pyfiglet import Figlet
from requests.exceptions import ConnectionError
from urllib3.exceptions import MaxRetryError

from misc_funcs import (bot, checkDataForMistakes, isNewPassportValid,
                        isUserIdValid, loadDataFromSettings, notify,
                        saveDataToSettings)
from rztk_checker import RZTKChecker
from web_checker import WebChecker


class Menu:
    def __init__(self) -> None:
        os.system('cls')
        self.__greet()
        self.main_menu = {
            1: self.startWorking,
            2: self._settingsMenu,
            3: self._exit
        }
        self.settings_menu = {
            1: self._webLoginChange,
            2: self._rozetkaLoginChange,
            3: self._userEditMenu,
            4: self.__botTokenChange,
            0: self._mainMenu
        }
        self.user_edit = {
            1: self.__addUser,
            2: self.__deleteUser,
            0: self._settingsMenu
        }
        self.data = loadDataFromSettings()
        self._mainMenu()
        

    def __greet(self):
        prev_text = Figlet(font="slant")
        print(prev_text.renderText("INFOPORT BOT"))

    def _mainMenu(self):
        self.__clear()
        try:
            user_input = int(
                input('\n'.join(
                    [
                        '1. Запуск бота',
                        '2. Настройки',
                        '3. Выход',
                        ''
                    ]
                    )
                )
            )
        except ValueError:
            self.__wrongInput()
            self._mainMenu()
        try:
            self.main_menu[user_input]()
        except KeyError:
            self.__wrongInput()
            self._mainMenu()

    def __clear(self):
        os.system('cls')
        self.__greet()

    def __wrongInput(self):
        print('Неверный ввод')
        time.sleep(1)
        self.__clear()

    def startWorking(self):
        self.__clear()
        if not checkDataForMistakes(data=self.data):
            print('\n', 'Не все данные заполнены в настройках.')
            time.sleep(3)
            self._mainMenu()
        print('Работаю... (Ctrl + C для завершения) ')
        web = WebChecker(login_data=self.data['WebLoginData'])
        rztk = RZTKChecker(login_data=self.data['RozetkaLoginData'])
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
        except MaxRetryError and ConnectionError:
            user_confirm = input('\n'.join(
                [
                    'Отсутствует подключение к интернету.',
                    '------------------------------------',
                    'Enter для возврата в главное меню.'
                ]
            ))
            self._mainMenu()
        except KeyboardInterrupt:
            self.__clear()
            print('Останавливаюсь...')
            del web, rztk
            time.sleep(1)
            self._mainMenu()

    def _settingsMenu(self):
        self.__clear()
        try:
            user_input = int(
                input('\n'.join(
                        [
                            '1. Изменить данные входа на сайт',
                            '2. Изменить данные входа на Rozetka',
                            '3. Управление пользователями',
                            '4. Изменить бот-токен для уведомлений',
                            '0. Назад',
                            ''
                        ]
                    )
                )
            )
        except ValueError:
            self.__wrongInput()
            self._settingsMenu()
        try:
            self.settings_menu[user_input]()
        except KeyError:
            self.__wrongInput()
            self._settingsMenu()

    def _webLoginChange(self):
        self.__clear()
        try:
            print(
                'Обновление данных логина для входа на сайт:',
                'Текущий пользователь: {}'.format(self.data['WebLoginData']['login']),
                sep='\n'
            )
        except IndexError:
            pass
        new_login = input('Новое имя пользователя: ')
        new_password = getpass('Новый пароль: ')
        if not isNewPassportValid(password=new_password):
            print('Данный пароль не подходит')
            self.__clear()
            time.sleep()
            new_password = getpass('Новый пароль: ')
        else:
            self.data['WebLoginData'] = {
                'login': new_login,
                'password': new_password
            }
        saveDataToSettings(self.data)
        self.__clear()
        print('Готово')
        time.sleep(1)
        self._mainMenu()

    def _rozetkaLoginChange(self):
        self.__clear()
        try:
            print(
                'Обновление данных логина для входа на сайт:',
                'Текущий пользователь: {}'.format(list(self.data['RozetkaLoginData'].keys())[0]),
                sep='\n'
            )
        except IndexError:
            pass
        new_login = input('Новое имя пользователя: ')
        new_password = getpass('Новый пароль: ')
        if not isNewPassportValid(password=new_password):
            print('Данный пароль не подходит')
            new_password = getpass('Новый пароль: ')
        else:
            self.data['RozetkaLoginData'] = {
                'login': new_login,
                'password': new_password
            }
        saveDataToSettings(self.data)
        self.__clear()
        print('Готово')
        time.sleep(1)
        self._mainMenu()

    def _userEditMenu(self):
        self.__clear()
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
            self._userEditMenu()
        try:
            self.user_edit[user_input]()
        except KeyError:
            self.__wrongInput()
            self._userEditMenu()
    
    def __botTokenChange(self):
        new_token = input('\n'.join(
            [
                'Введите новый бот-токен: ',
                '0. Назад',
                ''
            ]
        ))
        if new_token == '0':
            self._settingsMenu()
        else:
            self.data['BotToken'] = new_token
            saveDataToSettings(self.data)
            print('Готово')
            time.sleep(1)
            self._settingsMenu()

    def __addUser(self):
        print(
            'Необходимо открыть бот @Infoport_Notification_bot.',
            'Далее, ввести команду /login, в ответ бот пришлет номер чата.',
            'После копирования номера от бота, необходимо нажать Ctrl + C',
            sep='\n'
        )
        try:
            bot.polling()
        except KeyboardInterrupt:
            bot.stop_polling()
            self.__clear()
        user_id = input('Введи номер полученный от бота: ')
        if isUserIdValid(user_id):
            user_name = input('Введи имя пользователя (латиницей): ')
        else:
            self.__wrongInput()
            self.__addUser()
        self.data['Users'].update({user_name: user_id})
        saveDataToSettings(self.data)
        print('Готово')
        time.sleep(1)
        self._mainMenu()
        

    
    def __deleteUser(self):
        self.__clear()
        print('Введи имя пользователя которого необходимо удалить:', end='\n')
        for index, user in enumerate(self.data['Users'].keys()):
            print(f'{index + 1}. {user}')
        print('0. Назад', end='\n')
        user_input = input()
        if user_input == '0':
            self._userEditMenu()
        elif user_input in self.data['Users'].keys():
            user_confirm = str(
                input(
                    f'Удалить пользователя {user_input}? Y/N '
                )
            )
            if user_confirm in 'Yy':
                self.data['Users'].pop(user_input)
                saveDataToSettings(data=self.data)
                print('Готово')
                time.sleep(1)
                self._mainMenu()
            else:
                self._mainMenu()
        else:
            self.__wrongInput()
            self.__deleteUser()

    def _exit(self):
        self.__clear()
        print('Закрываемся...')
        time.sleep(1)
        sys.exit()
