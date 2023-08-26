import requests
import json
from config import keys

class ConvertionException(Exception):
    pass

class ConvertorValute:
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        if quote == base:
            raise ConvertionException(f'Ну и зачем тебе перевод {quote} в {base}?\nВведи нормальный запрос:\nПараметров \
должно быть "3"\n(Конвертироваемая, целевая, количество валюты)')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f'Я не умею обрабатывать валюту {quote}.\nЕщё не научился, все вопросы к автору.')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f'Я не умею обрабатывать валюту {base}.\nЕщё не научился, все вопросы к автору.')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Ты серьёзно решил(а) перевести цифру "{amount}"?\nДавай по-новой...')

        date = requests.get(f'https://v6.exchangerate-api.com/v6/d4b3317c3f6e87ca27ca349a/pair/{quote_ticker}/{base_ticker}')
        j_unzip = json.loads(date.content)['conversion_rate']
        result = j_unzip * amount

        return result