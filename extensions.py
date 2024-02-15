import requests
import json
from config import keys


class APIException(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise APIException(f'Невозможно конвертировать одинаковые валюты "{base}".')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f"В списке валют /values нет валюты {quote}.")

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f"В списке доступных валют нет валюты {base}.")

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f"Введите корректное количество. В параметр количества переводимой валюты вы ввели: {amount}.")

        if float(amount) < 0:
            raise APIException(f"Количество переводимой валюты не может быть меньше '0'")

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]]

        return total_base * amount
