from ticker import technicalanalysis as ta
from ticker import tickerdata as td
from ticker import plotter as pl


df = td.tickerdata('AMZN').gettickerdata()
df.to_csv('tickerdata.csv')
df = ta.technicalanalysis().analyze(df)
df.to_csv('analysisdata.csv')
pl.plotter().plot(df)