import requests
import json
from config import keys

class ConvertionException(Exception):
    pass

class ConvertorValute:
    # И я прекрасно понимаю что:
    #   1. Данный алгоритм протеворечит принципам ООП
    #   2. Если валют станет больше, то и if`ов (Возиожных комбинаций после ввода пользователя) писать придётся больше.
    #   Тем более что количество будет возрастать в геометрической прогрессии.
    # Но я хотел реализовать отечественный продукт, максимально просто, как могу представить.
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        if quote == base:
            raise ConvertionException(f'Ну и зачем тебе перевод {quote} в {base}?\n Введи нормальный запрос:\nПараметров \
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
            raise ConvertionException(f'Ты серьёзно решил(а) перевести цифру {amount}?\nДавай по-новой...')

        date = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
        USD = date['Valute']['USD']['Value']
        EUR = date['Valute']['EUR']['Value']

        if quote_ticker != 'RUB':
            if quote_ticker == 'USD' and base_ticker == 'EUR':
                result = amount * USD / EUR
            elif quote_ticker == 'EUR' and base_ticker == 'USD':
                result = amount * EUR / USD
            elif quote_ticker == 'USD':
                result = USD * amount
            elif quote_ticker == 'EUR':
                result = EUR * amount
        else:
            if base_ticker == 'USD':
                result = amount / USD
            elif base_ticker == 'EUR':
                result = amount / EUR

        return result
