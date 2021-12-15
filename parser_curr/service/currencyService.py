from parser_curr.domain.currency import Currency
from parser_curr.processor.parserProcessor import Parser
from os.path import exists
import requests
import csv
import re

class CurrencyService:

    @staticmethod
    def getCurrencyByDate(date, currencies):
        result = []

        currencies = currencies.split(',') if currencies else []
        alpha_pattern = r'[A-Z]{3}'
        alphas = []
        for code in currencies:
            if not code:
                continue
            if re.fullmatch(pattern=alpha_pattern, string=code):
                alphas.append(code)
            else:
                raise ValueError(f'Invalid format of code "{code}"')

        filename = str(date).replace('.', '_') + '.csv'

        if exists(filename):
            print("-----------------------USE CACHE------------------------------")
            file = open(filename, mode='r')
            reader = csv.reader(file)
            header = next(reader)
            rows = []
            for row in reader:
                rows.append(row)
                if row:
                    for currency in currencies:
                        if row.__getitem__(1).__contains__(currency):
                            result.append(Currency(row.__getitem__(0), row.__getitem__(1), row.__getitem__(2), row.__getitem__(3), row.__getitem__(4), row.__getitem__(5)))
            file.close()
        else:
            print("-----------------------DO HTTP REQUEST------------------------------")
            html = requests.get(
                fr'http://www.cbr.ru/currency_base/daily/?UniDbQuery.Posted=True&UniDbQuery.To=%s', date).text
            data = Parser(text=html).get_curr_info()

            file = open(file=filename, mode='w')
            header = ['numeric_code', 'alpha_code', 'quantity', 'text', 'value', 'base_value']
            writer = csv.writer(file)
            writer.writerow(header)
            for currency in data.currencies:
                row = [currency.numeric_code, currency.alpha_code, currency.quantity, currency.text, currency.value, currency.base_value]
                writer.writerow(row)
                if currencies.__contains__(currency.alpha_code):
                    result.append(currency)
            file.close()
        return result