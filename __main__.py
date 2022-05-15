from ticker import ta_macd as tamacd
from ticker import ta_stoch as tastoch
from ticker import tickerdata as td
import logging
logging.basicConfig(level=logging.DEBUG)


class main:
    def macd(self, ticker, techanalysis):
        df = td.tickerdata(ticker).gettickerdata()
        df.to_csv(techanalysis+'_'+ticker+'tickerdata.csv')
        macd = tamacd.macd()
        df = macd.getanalysisdata(df)
        df.to_csv(techanalysis+'_'+ticker+'analysisdata.csv')
        df = macd.applystrategy(df)
        df.to_csv(techanalysis+'_'+ticker+'strategy.csv')
        dfaccounting = macd.strategyanalyzer(df)
        print(dfaccounting)
        dfaccounting.to_csv(techanalysis+'_'+ticker+'accounting.csv')
        macd.plot(df, ticker, dfaccounting)

    def stoch(self, ticker, techanalysis):
        df = td.tickerdata(ticker).gettickerdata()
        df.to_csv(techanalysis+'_'+ticker+'tickerdata.csv')
        stoch = tastoch.stoch()
        df = stoch.getanalysisdata(df)
        df.to_csv(techanalysis+'_'+ticker+'analysisdata.csv')
        # df = macd.applystrategy(df)
        # df.to_csv(techanalysis+'_'+ticker+'strategy.csv')
        # dfaccounting = macd.strategyanalyzer(df)
        # print(dfaccounting)
        # dfaccounting.to_csv(techanalysis+'_'+ticker+'accounting.csv')
        stoch.plot(df, ticker)


x = main()
x.macd('AMZN', 'macd')
x.stoch('AMZN', 'stoch')
