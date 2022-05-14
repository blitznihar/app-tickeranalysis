
import logging
import yfinance as yf
import pandas_ta as ta
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import numpy as np
import csv


class technicalanalysis:

    def analyze(self, df):
        logging.info("technicalanalysis: starting")
        df.ta.macd(close='close', fast=12, slow=26, append=True)
        logging.info("technicalanalysis: done")
        return df
