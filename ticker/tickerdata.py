import logging
import yfinance as yf
import csv


class tickerdata:
    def __init__(self, ticker):
        self.ticker = ticker

    def gettickerdata(self, period='1y', interval='1d'):
        logging.info("technicalanalysis: fetching")
        return yf.Ticker(self.ticker).history(interval=interval, period=period)[map(str.title, ['open', 'close', 'low', 'high', 'volume'])]
