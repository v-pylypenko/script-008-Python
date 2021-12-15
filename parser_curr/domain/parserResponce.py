from parser_curr.domain.currency import Currency


class ParserResponse:

    def __init__(self, date, currencies):
        self.date = date
        self.currencies = currencies
