from parser_curr.parser import Parser
import requests
import logging

def main():
    try:
        print(Parser(text=requests.get("http://www.cbr.ru/currency_base/daily/?UniDbQuery.Posted=True&UniDbQuery.To=13.12.2021").text, currencies="USD,HKD").get_curr_info())

    except Exception as err:
        logging.error(err)

if __name__ == '__main__':
    main()
