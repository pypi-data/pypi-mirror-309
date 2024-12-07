import re

import click
import requests
from webrequests import WebRequest as WR
from prettytable import PrettyTable


class XueQiu(object):
    base_url = 'https://xueqiu.com'

    def __init__(self):
        self.session = requests.Session()
        resp = WR.get_response(self.base_url, session=self.session)
        if resp.status_code != 200:
            print('ERROR:', resp.text)

    def search(self, name):
        """查询关键词"""
        url = f'https://xueqiu.com/query/v1/search/web/stock.json?q={name}'
        resp = WR.get_response(url, session=self.session)
        codes = resp.json()['list']
        if codes:
            return codes[0]['code']

    def check_symbol(self, *symbols):
        code_pattern = re.compile(f'^S[HZ]\d{6}$')
        codes = []
        for symbol in symbols:
            if not code_pattern.match(symbol):
                query_symbol = self.search(symbol)
                if not query_symbol:
                    click.echo(f'bad query: {query_symbol}')
                    continue
                symbol = query_symbol
            codes.append(symbol)
        return codes

    def quote(self, *symbols):
        """报价"""
        symbol = ','.join(symbols)
        url = f'https://stock.xueqiu.com/v5/stock/batch/quote.json?symbol={symbol}'
        data = WR.get_response(url, session=self.session).json()['data']
        quotes = [item['quote'] for item in data['items']]
        return quotes

    # def minute(self, symbol, period=1):
    #     """分时
    #     period: 1 or 5
    #     """
    #     url = f'https://stock.xueqiu.com/v5/stock/chart/minute.json?symbol={symbol}&period={period}d'

    # def kline(self, symbol):
    #     url = f'https://stock.xueqiu.com/v5/stock/chart/kline.json?symbol=SH600601&begin=1688744151892&period=day&type=before&count=-284&indicator=kline,pe,pb,ps,pcf,market_capital,agt,ggt,balance'

    @staticmethod
    def show_table(quotes, reverse=True):
        fields = ['symbol', 'name', 'percent', 'chg', 'current']
        table = PrettyTable(fields)

        quotes = sorted(quotes, key=lambda x: x['percent'], reverse=reverse)

        for quote in quotes:
            percent = quote['percent'] or 0

            if percent > 0:
                color = 'red'
                percent = f'+{percent}'
                quote['chg'] = f'+{quote["chg"]}'
            elif percent < 0:
                color = 'green'
            else:
                color = None
            quote['percent'] = click.style(f'{percent}%', fg=color)
            row = list(map(quote.get, fields))
            table.add_row(row)

        table.align['percent'] = 'r'
        table.add_autoindex('index')
        return table
