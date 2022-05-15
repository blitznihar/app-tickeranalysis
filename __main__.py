from ticker import ta_macd as ta
from ticker import tickerdata as td
import logging
logging.basicConfig(level=logging.DEBUG)


class main:
    def macd(self, ticker, techanalysis):
        df = td.tickerdata(ticker).gettickerdata()
        df.to_csv(techanalysis+'_'+ticker+'tickerdata.csv')
        macd = ta.macd()
        df = macd.getanalysisdata(df)
        df.to_csv(techanalysis+'_'+ticker+'analysisdata.csv')
        df = macd.applystrategy(df)
        df.to_csv(techanalysis+'_'+ticker+'strategy.csv')
        dfaccounting = macd.strategyanalyzer(df)
        print(dfaccounting)
        dfaccounting.to_csv(techanalysis+'_'+ticker+'accounting.csv')
        macd.plot(df, ticker, dfaccounting)


x = main()
x.macd('AMZN', 'macd')
