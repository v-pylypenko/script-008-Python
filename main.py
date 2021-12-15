from parser_curr.service.currencyService import CurrencyService
import logging

logging.basicConfig(level=logging.INFO)

def main():
    try:
        currencies = CurrencyService.getCurrencyByDate(date="13.12.2021", currencies="USD,HKD")
        for currency in currencies:
            print(currency.alpha_code + ' ' + currency.value)
    except Exception as err:
        logging.error(err)

if __name__ == '__main__':
    main()
