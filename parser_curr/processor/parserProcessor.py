import re
import decimal
from parser_curr.domain.parserResponce import ParserResponse
from parser_curr.domain.currency import Currency


def get_pattern():
    return re.compile(
        r'[\s]+<tr>[\r\n]+[\s]+<td>(\d{3})</td>[\r\n]+[\s]+<td>([A-Z]{3})</td>[\r\n]+[\s]+<td>(\d+)</td>'
        r'[\r\n]+[\s]+<td>([А-Яа-я ]+)</td>[\r\n]+[\s]+<td>([0-9,]+)</td>[\r\n]+[\s]+</tr>')


class Parser:
    def __init__(self, text):
        self.text = text

    def get_curr_info(self):
        pattern = get_pattern()

        currencies = []

        for match in pattern.finditer(self.text):
            numeric_code = match[1]
            alpha_code = match[2]
            quantity = match[3]
            text = match[4]
            value = match[5].replace(',', '.')
            base_value = str(decimal.Decimal(match[5].replace(',', '.')) / decimal.Decimal(match[3]))
            currencies.append(Currency(numeric_code, alpha_code, quantity, text, value, base_value))

        data = ParserResponse(self.get_current_date(), currencies)

        return data

    def get_current_date(self):
        pattern = re.compile(r' value="(\d{2}\.\d{2}\.\d{4})" ')
        match = pattern.search(self.text)

        return match[1] if match else None

    @staticmethod
    def check_date(date):
        date_pattern = r'\d{2}\.\d{2}\.\d{4}'

        return re.fullmatch(pattern=date_pattern, string=str(date))
