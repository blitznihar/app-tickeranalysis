from ticker import ta_macd as tamacd
from ticker import ta_stoch as tastoch
from ticker import tickerdata as td
import logging
logging.basicConfig(level=logging.DEBUG)


class main:

    def fetchdata(self, ticker):
        df = td.tickerdata(ticker).gettickerdata()
        df.to_csv(ticker+'tickerdata.csv')
        return df

    def process(self, ticker, df, technicalanalysis):
        df = technicalanalysis.getanalysisdata(df)   
        df.to_csv(technicalanalysis.gettatype()+'_'+ticker+'analysisdata.csv')
        df = technicalanalysis.applystrategy(df)
        df.to_csv(technicalanalysis.gettatype() +'_'+ticker+'strategy.csv')
        dfaccounting = technicalanalysis.strategyanalyzer(df)
        dfaccounting.to_csv(technicalanalysis.gettatype()+'_'+ticker+'accounting.csv')
        technicalanalysis.plot(df, ticker, dfaccounting)


x = main()
ticker = 'QQQ'
df = x.fetchdata(ticker)

technicalanalysis = tastoch.stoch()
x.process(ticker,  df, technicalanalysis)

technicalanalysis = tamacd.macd()
x.process(ticker, df, technicalanalysis)
