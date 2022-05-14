
import logging
import yfinance as yf
import pandas_ta as ta
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import numpy as np
import csv

class tickeranalysis:
    def __init__(self, ticker):
        self.ticker = ticker

    def gettickerdata(self, period='1y', interval='1d'):
        logging.info("technicalanalysis: fetching")
        return yf.Ticker(self.ticker).history(interval=interval, period=period)[map(str.title, ['open', 'close', 'low', 'high', 'volume'])]

    def technicalanalysis(self, df):
        logging.info("technicalanalysis: starting")
        df.ta.macd(close='close', fast=12, slow=26, append=True)
        logging.info("technicalanalysis: done")
        return df

    def exportdata(self, df, filename='file_name.csv'):
        logging.info("exportdata: {0}", format(filename))
        df.to_csv(filename)

    def plot(self, df):
        logging.info("plot: started")
        logging.info(df)
        fig = make_subplots(rows=2, cols=1)
        # price Line
        fig.append_trace(
            go.Scatter(
                x=df.index,
                y=df['open'],
                line=dict(color='#110af2', width=1),
                name='open',
                # showlegend=False,
                legendgroup='1',

            ), row=1, col=1
        )

        # Candlestick chart for pricing
        fig.append_trace(
            go.Candlestick(
                x=df.index,
                open=df['open'],
                high=df['high'],
                low=df['low'],
                close=df['close'],
                increasing_line_color='#ff0000',
                decreasing_line_color='#00ff00',
                showlegend=False

            ), row=1, col=1
        )

        # Fast Signal (%k)
        fig.append_trace(
            go.Scatter(
                x=df.index,
                y=df['macd_12_26_9'],
                line=dict(color='#ff9900', width=2),
                name='macd',
                # showlegend=False,
                legendgroup='2',

            ), row=2, col=1
        )

        # Slow signal (%d)
        fig.append_trace(
            go.Scatter(
                x=df.index,
                y=df['macds_12_26_9'],
                line=dict(color='#000000', width=2),
                # showlegend=False,
                legendgroup='2',
                name='signal'
            ), row=2, col=1
        )

        # Colorize the histogram values
        colors = np.where(df['macdh_12_26_9'] < 0, '#00ff00', '#ff0000')

        # Plot the histogram
        fig.append_trace(
            go.Bar(
                x=df.index,
                y=df['macdh_12_26_9'],
                name='histogram',
                marker_color=colors,

            ), row=2, col=1
        )

        # Make it pretty
        layout = go.Layout(
            plot_bgcolor='#efefef',
            # Font Families
            font_family='Monospace',
            font_color='#000000',
            font_size=20,
            xaxis=dict(
                rangeslider=dict(
                    visible=False
                )
            )
        )
        fig.update_yaxes(title_text="Price", row=1, col=1)
        fig.update_yaxes(title_text="MACD", row=2, col=1)
        # Update options and show plot
        fig.update_layout(layout)
        fig.show()
