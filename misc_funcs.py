import base64
import re


def morphDataToNotify(
    source: str,
    order_id: str,
    customer_name: str,
    customer_phone: str,
    products: list,
    total_cost: str
) -> str:
    return '\n'.join(
        [
            f'{source}',
            '=============',
            f'Поступил заказ #{order_id}',
            '=============',
            f'Покупатель: {customer_name}',
            f'Телефон: {customer_phone}',
            '=============',
            '\n---------------------------\n'.join(products),
            '=============',
            f'Итоговая сумма: {total_cost} грн'
        ]
    )


def passwordEncode(password) -> str:
    password_encode = str(password).encode('UTF-8')
    password = base64.b64encode(password_encode)
    return password.decode('UTF-8')


def exceptHtml(order: list) -> list:
    pattern = r'<[^>]*>'
    clear_list = [re.sub(pattern, '', str(item)) for item in order]
    clear_list[5] = ''
    return [item for item in clear_list if item != '']
