MAIN_MENU = "\n".join(
                        [
                            "1.[bold] Запуск бота [/bold]",
                            "2.[bold] Настройки [/bold]",
                            "0.[bold] Выход [/bold]",
                            ""
                        ]
                    )

SETTINGS_MENU = "\n".join(
                        [
                            "1.[bold] Изменить данные входа на сайт [/bold]",
                            "2.[bold] Изменить данные входа на Rozetka [/bold]",
                            "3.[bold] Изменить бот-токен для уведомлений [/bold]",
                            "4.[bold] Управление пользователями [/bold]",
                            "0.[bold] Назад [/bold]",
                            "",
                        ]
                    )

USER_EDIT_MENU = "\n".join(
                        [
                            "1.[bold] Добавить нового пользователя [/bold]",
                            "2.[bold] Удалить пользователя [/bold]",
                            "0.[bold] Назад [/bold]",
                            "",
                        ]
                    )

LOGIN_CHANGE = "\n".join(
                [
                    "0.[bold] Назад [/bold]",
                    "[bold]Новое имя пользователя: [/bold]",
                ]
            )

TOKEN_CHANGE = "\n".join(
                [
                    "[bold]0. Назад[/bold]",
                    "[bold]Введите новый бот-токен: [/bold]"
                ]
            )

NO_CONNECTION = '\n'.join(
    [
        '[bold]-------------------------------[/bold]',
        '[bold]--НЕТ ПОДКЛЮЧЕНИЯ К ИНТЕРНЕТУ--[/bold]',
        '[bold]-------------------------------[/bold]'
    ]
)

SETTINGS_ERROR = '\n'.join(
    [
        '[bold]-------------------------------[/bold]',
        '[bold]------НЕДОСТАТОЧНО ДАННЫХ------[/bold]',
        '[bold]-------------------------------[/bold]'
    ]
)

WRONG_INPUT = '\n'.join(
    [
        '[bold]-------------------------------[/bold]',
        '[bold]---------НЕВЕРНЫЙ ВВОД---------[/bold]',
        '[bold]-------------------------------[/bold]'
    ]
)

HEADERS = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36 OPR/85.0.4341.79'
        }

PASSWORD = '[bold]Новый пароль: [/bold]'

WRONG_PASSWORD = '\n'.join(
    [
        '[bold]-------------------------------[/bold]',
        '[bold]---ДАННЫЙ ПАРОЛЬ НЕ ПОДХОДИТ---[/bold]',
        '[bold]-------------------------------[/bold]'
    ]
)

USER_INPUT = '\n[bold]Выбери пункт меню... [/bold]'

WORKING = '[bold]Работаю... [/bold]'

STOPING = '[bold]Останавливаюсь...[/bold]'

EXIT = '[bold]Закрываемся...[/bold]'

NO_BOT_TOKEN = '\n'.join(
    [
        '[bold]-------------------------------[/bold]',
        '[bold]---Нужно добавить токен бота---[/bold]',
        '[bold]-------------------------------[/bold]'
    ]
)

USER_ADD_FAQ = '\n'.join(
    [
        "[bold]Необходимо открыть бот @Infoport_Notification_bot.[/bold]",
        "[bold]Далее, ввести команду /login, в ответ бот пришлет номер чата.[/bold]",
        "[bold]После копирования номера от бота, необходимо нажать Ctrl + C[/bold]",
    ]
)

USER_ID = '[bold]Введи номер полученный от бота: [/bold]'

USER_NAME = '[bold]Введи имя пользователя (латиницей): [/bold]'

DONE = '[bold]Готово[/bold]'