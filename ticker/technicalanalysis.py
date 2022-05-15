
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

class macd:

    def getanalysisdata(self, df):
        logging.info("technicalanalysis: starting")
        df.ta.macd(close='close', fast=12, slow=26, append=True)
        logging.info("technicalanalysis: done")
        return df

    def plot(self, df, ticker, dfaccounting):
        logging.info("plot: started")
        df.columns = [x.lower() for x in df.columns]

        fig = make_subplots(
            rows=3, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.05,
            specs=[[{"type": "scatter"}],
                    [{"type": "scatter"}],
                    [{"type": "table"}]]
        )
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
        fig.append_trace(
            go.Scatter(
                mode='markers',
                x=df.index,
                y=df['buysignal'],
                marker_symbol='triangle-up',
                marker_line_width=2, 
                marker_size=10,
                marker_color='purple',
                showlegend=True,
            ), row=1, col=1
        )
        fig.append_trace(
            go.Scatter(
                mode='markers',
                x=df.index,
                y=df['sellsignal'],
                marker_symbol='triangle-down',
                marker_line_width=2, 
                marker_size=10,
                marker_color='pink',
                showlegend=True
            ), row=1, col=1
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
            font_size=15,
            xaxis=dict(
                rangeslider=dict(
                    visible=False
                )
            ), title_text=ticker
        )
        
        table_obj = go.Table(
            header=dict(values=list(dfaccounting.columns), fill_color='paleturquoise', align='left', font=dict(size=10)),
            cells=dict(
                values=dfaccounting.transpose().values.tolist(), 
                fill_color='lavender', 
                align='left', 
                font=dict(size=10))
        )
        fig.append_trace(table_obj, row=3, col=1)
        # Update options and show plot
        fig.update_layout(layout)
        fig.show()

    def plottable(self, dfaccounting):
        fig = make_subplots(rows=1, cols=1)
        table_obj = go.Table(
            header=dict(values=list(dfaccounting.columns), fill_color='paleturquoise', align='left'),
            cells=dict(values=dfaccounting.transpose().values.tolist(), fill_color='lavender', align='left')
        )
        fig.append_trace(table_obj, row=3, col=1)
        fig.show()
    
    def applystrategy(self, df):
        df.columns = [x.lower() for x in df.columns]
        signal_Buy = []
        signal_Sell = []
        position = False
        for i in range(len(df)):
            if df['macdh_12_26_9'][i-1]>0 and df['macdh_12_26_9'][i]<0 and position == True:
                signal_Sell.append(df['open'][i])
                signal_Buy.append(np.nan)
                position = False
            elif df['macdh_12_26_9'][i-1]<0 and df['macdh_12_26_9'][i]>0: 
                signal_Buy.append(df['open'][i])
                signal_Sell.append(np.nan)
                position = True
            else:
                signal_Buy.append(np.nan)
                signal_Sell.append(np.nan)
        df['buysignal'] = signal_Buy
        df['sellsignal'] = signal_Sell
        return df

    def strategyanalyzer(self, df):
        df.columns = [x.lower() for x in df.columns]
        signal_Buy = []
        signal_Sell = []
        buyingdate = []
        sellingdate = []
        buyingprice = []
        sellingprice = []
        profit = [] 
        for i in range(len(df)):
           if df['buysignal'][i] > 0:
               buyingprice.append(df['buysignal'][i])
               buyingpricei = df['buysignal'][i]
               buyingdate.append(df.index[i])
           elif df['sellsignal'][i] > 0:
                sellingprice.append(df['sellsignal'][i])
                sellingpricei=df['sellsignal'][i]
                sellingdate.append(df.index[i])
                profit.append(sellingpricei - buyingpricei)
        print(sellingdate)
        print(profit)
        accountingset = {
            'buyingprice': buyingprice,
            'buydate': buyingdate,
            'sellingprice': sellingprice,
            'selldate': sellingdate,
            'profit': profit
            }
        dfaccounting = pd.DataFrame(accountingset)
        return dfaccounting
