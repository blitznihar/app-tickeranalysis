
import logging
from pickletools import markobject
from symtable import Symbol
import pandas_ta as ta
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import numpy as np
import csv
import plotly.figure_factory as ff
from ticker import ta_common as ta

class macd(ta.common):

    def runanalysis(self, df):
        df.ta.macd(close='close', fast=12, slow=26, append=True)
        return df

    def buyrule(self, df, i):
        return df[self.fastline()][i-1] < df[self.slowline()][i-1] and df[self.fastline()][i] > df[self.slowline()][i]
    
    def sellrule(self, df, i):
        return df[self.fastline()][i-1] > df[self.slowline()][i-1] and df[self.fastline()][i] < df[self.slowline()][i]

    def fastline(self):
        return 'macd_12_26_9'

    def slowline(self):
        return 'macds_12_26_9'
    
    def gettatype(self):
        return 'MACD'