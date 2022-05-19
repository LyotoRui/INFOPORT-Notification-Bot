MAIN_MENU = "\n".join(
                        [
                            "1. Запуск бота",
                            "2. Настройки",
                            "3. Выход",
                            ""
                        ]
                    )

SETTINGS_MENU = "\n".join(
                        [
                            "1. Изменить данные входа на сайт",
                            "2. Изменить данные входа на Rozetka",
                            "3. Управление пользователями",
                            "4. Изменить бот-токен для уведомлений",
                            "0. Назад",
                            "",
                        ]
                    )

USER_EDIT_MENU = "\n".join(
                        [
                            "1. Добавить нового пользователя",
                            "2. Удалить пользователя",
                            "0. Назад",
                            "",
                        ]
                    )

LOGIN_CHANGE = "\n".join(
                [
                    "0. Назад",
                    "Новое имя пользователя: ",
                ]
            )

CONNECTION_FAILED = "\n".join(
                    [
                        "Отсутствует подключение к интернету.",
                        "------------------------------------",
                        "Enter для возврата в главное меню.",
                    ]
                )

HEADERS = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36 OPR/85.0.4341.79'
        }