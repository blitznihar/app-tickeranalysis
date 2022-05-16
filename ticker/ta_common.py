
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


class common:

    def getanalysisdata(self, df):  # COMMON
        logging.info("technicalanalysis: starting")
        df = self.runanalysis(df)
        logging.info("technicalanalysis: done")
        return df

    def plot(self, df, ticker, dfaccounting):  # COMMON WITH LOT OF MODIFICATIONS
        logging.info("plot: started")
        df.columns = [x.lower() for x in df.columns]
        # Create our primary chart
        # the rows/cols arguments tell plotly we want two figures
        fig = make_subplots(
            rows=3, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.05,
            specs=[[{"type": "scatter"}],
                   [{"type": "scatter"}],
                   [{"type": "table"}]]
        )
        # Create our Candlestick chart with an overlaid price line
        fig.append_trace(
            go.Candlestick(
                x=df.index,
                open=df['open'],
                high=df['high'],
                low=df['low'],
                close=df['close'],
                increasing_line_color='#ff9900',
                decreasing_line_color='black',
                showlegend=False
            ), row=1, col=1  # <------------ upper chart
        )
        # price Line
        fig.append_trace(
            go.Scatter(
                x=df.index,
                y=df['open'],
                line=dict(color='#ff9900', width=1),
                name='open',
            ), row=1, col=1  # <------------ upper chart
        )

        # Fast Signal (%k)
        fig.append_trace(
            go.Scatter(
                x=df.index,
                y=df[self.fastline()],
                line=dict(color='#ff9900', width=2),
                name='fast',
            ), row=2, col=1  # <------------ lower chart
        )
        # Slow signal (%d)
        fig.append_trace(
            go.Scatter(
                x=df.index,
                y=df[self.slowline()],
                line=dict(color='#000000', width=2),
                name='slow'
            ), row=2, col=1  # <------------ lower chart
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
        # Extend our y-axis a bit
        fig.update_yaxes(range=[-10, 110], row=2, col=1)
        # Add upper/lower bounds
        fig.add_hline(y=0, col=1, row=2, line_color="#666", line_width=2)
        fig.add_hline(y=100, col=1, row=2, line_color="#666", line_width=2)
        # Add overbought/oversold
        fig.add_hline(y=20, col=1, row=2, line_color='#336699',
                      line_width=2, line_dash='dash')
        fig.add_hline(y=80, col=1, row=2, line_color='#336699',
                      line_width=2, line_dash='dash')
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
            ), title_text=ticker +'-'+ self.gettatype()
        )
        table_obj = go.Table(
            header=dict(values=list(dfaccounting.columns),
                        fill_color='paleturquoise', align='left', font=dict(size=10)),
            cells=dict(
                values=dfaccounting.transpose().values.tolist(),
                fill_color='lavender',
                align='left',
                font=dict(size=10))
        )
        fig.append_trace(table_obj, row=3, col=1)
        fig.update_layout(layout)
        # View our chart in the system default HTML viewer (Chrome, Firefox, etc.)
        fig.show()

    def applystrategy(self, df):  # COMMON WITH RULE MODIFICATIONS
        df.columns = [x.lower() for x in df.columns]
        signal_Buy = []
        signal_Sell = []
        position = False
        for i in range(len(df)):
            if self.sellrule(df,i) and position == True:
                signal_Sell.append(df['open'][i])
                signal_Buy.append(np.nan)
                position = False
            elif self.buyrule(df,i):
                signal_Buy.append(df['open'][i])
                signal_Sell.append(np.nan)
                position = True
            else:
                signal_Buy.append(np.nan)
                signal_Sell.append(np.nan)
        df['buysignal'] = signal_Buy
        df['sellsignal'] = signal_Sell
        return df

    def strategyanalyzer(self, df):  # COMMON
        df.columns = [x.lower() for x in df.columns]
        buyingdate = []
        sellingdate = []
        buyingprice = []
        sellingprice = []
        profit = []
        total = []
        for i in range(len(df)):
            if df['buysignal'][i] > 0:
                buyingprice.append(df['buysignal'][i])
                buyingpricei = df['buysignal'][i]
                buyingdate.append(df.index[i])
            elif df['sellsignal'][i] > 0:
                sellingprice.append(df['sellsignal'][i])
                sellingpricei = df['sellsignal'][i]
                sellingdate.append(df.index[i])
                profit.append(sellingpricei - buyingpricei)
        for i in range(len(profit)):
            if(len(total) == 0):
                total.append(profit[i])
            else:
                total.append(profit[i] + total[i-1])

# there is a buy but no sell so need to manipulate

        if len(buyingprice) > len(sellingprice):
            sellingprice.append(np.nan)
            profit.append(np.nan)
            total.append(total[len(total)-1])
            sellingdate.append(pd.NaT)

        accountingset = {
            'buyingprice': buyingprice,
            'buydate': buyingdate,
            'sellingprice': sellingprice,
            'selldate': sellingdate,
            'profit': profit,
            'total': total
        }

        dfaccounting = pd.DataFrame(accountingset)
        dfaccounting['buydate'] = dfaccounting['buydate'].dt.strftime(
            '%m-%d-%Y')
        dfaccounting['selldate'] = dfaccounting['selldate'].dt.strftime(
            '%m-%d-%Y')
        dfaccounting['sellingprice'] = dfaccounting['sellingprice'].apply(
            lambda x: round(x, 2))
        dfaccounting['buyingprice'] = dfaccounting['buyingprice'].apply(
            lambda x: round(x, 2))
        dfaccounting['profit'] = dfaccounting['profit'].apply(
            lambda x: round(x, 2))
        dfaccounting['total'] = dfaccounting['total'].apply(
            lambda x: round(x, 2))
        return dfaccounting

    def runanalysis(self, df):
        pass

    def buyrule(self, df, i):
        pass

    def sellrule(self, df, i):
        pass

    def fastline(self):
        pass

    def slowline(self):
        pass

    def gettatype(self):
        pass