from ticker import tickeranalysis


x = tickeranalysis.tickeranalysis('AMZN')
df = x.gettickerdata()
x.exportdata(df,'tickerdata.csv')
df = x.technicalanalysis(df)
x.exportdata(df,'analysisdata.csv')
x.plot(df)