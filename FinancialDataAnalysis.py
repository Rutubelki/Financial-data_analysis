import pandas
import pandas as pan
import numpy
import datetime
import matplotlib.pyplot as plt
import pandas_datareader.data as remotedata
from datetime import date, datetime, time, timezone
import yfinance as yfin

yfin.pdr_override()
# Current Stock Value

#Step 1 - 3:
# Gather the data from Remote Data Repositories (Yahoo)
# Setting the Period be from 1st, January 2020 till Date
# Create a function called as get_stock_data() which takes ticker, start and end as params
def Get_Stock_Data(Ticker,start,end):
    data = remotedata.get_data_yahoo(Ticker, start, end)
    data.insert(0,"Ticker",Ticker)
    return data


Ticker = 'DIS'
start = datetime(2020,1,1)
end = datetime.today()

# Step 4:
# Create a pivot information
d = Get_Stock_Data(Ticker,start,end)
d.pivot(index=None,columns='Ticker',values='Close')

# Step 5:
# Create multiple dataframes for the following tickers: (IBM, CTS, TCS, BIS, SPY)
IBM = Get_Stock_Data('IBM',start,end)
CTS = Get_Stock_Data('CTS',start,end)
TCS = Get_Stock_Data('TCS',start,end)
BIS = Get_Stock_Data('BIS',start,end)
SPY = Get_Stock_Data('SPY',start,end)

# Step 6:
# Create pivot per dataframe
IBM = IBM.pivot(index=None,columns='Ticker',values='Close')
CTS = CTS.pivot(index=None,columns='Ticker',values='Close')
TCS = TCS.pivot(index=None,columns='Ticker',values='Close')
BIS = BIS.pivot(index=None,columns='Ticker',values='Close')
SPY = SPY.pivot(index=None,columns='Ticker',values='Close')

# Step 7:
# Combine the pivots into one single dataframe using panda function called concat()
mystock = pandas.concat([IBM,CTS,TCS,BIS,SPY], axis=1, join='outer')

# Step 8:
# Draw the plot
plt.style.use('ggplot')
mystock.plot(figsize=(40,20))
plt.title("My Stocks")
plt.show()

# Step 9:
# Create a covid_stock from the combined pivot for the given time period
covid_stocks = mystock['2020-2-1':'2020-7-31']

# Step 10:
# Plot the graph
plt.style.use('ggplot')
covid_stocks.plot(figsize=(40,20))
plt.title("Covid Stocks")
plt.show()

# Step 11:
# From the entries in the data frame choose 4 different stocks and create the plots

x = covid_stocks.index
covid_ibm_y = covid_stocks[['IBM']]
covid_spy_y = covid_stocks[['SPY']]
covid_cts_y = covid_stocks[['CTS']]
covid_tcs_y = covid_stocks[['TCS']]
covid_bis_y = covid_stocks[['BIS']]

fig, axes = plt.subplots(1,2,figsize=(15,5))
axes[0].plot(x,covid_ibm_y)
axes[1].plot(x,covid_tcs_y)
fig.suptitle('Covid 19 Affected Stocks')
plt.legend()
plt.show()

# Step 12:
# Getting information about a specific stock

Ticker = 'IBM'
start = datetime(2020,1,1)
end = datetime.today()
volume_dataframe = Get_Stock_Data(Ticker,start,end)
# Step 13:
# Dropping all the column except volume

volume_dataframe.drop(['Ticker','High','Low','Open','Close','Adj Close'],axis=1,inplace=True)

# Step 14:
# using bar chart to display the data
x = volume_dataframe.index
y = volume_dataframe['Volume']
plt.figure(figsize=(15,3))
plt.bar(x,y)
plt.show()

#calulating the percentage change:
print(mystock['IBM'])
print(mystock['IBM'].shift(1))
IBM_daily_percent_change = (mystock['IBM']/mystock['IBM'].shift(1)-1)*100
print(IBM_daily_percent_change)
IBM_daily_percent_change.plot()
plt.show()

IBM_daily_percent_change.iloc[0] = 0
plt.hist(IBM_daily_percent_change)
plt.show()

#Calculate the daily stock price changes

daiy_change = (mystock-mystock.shift(1))/mystock.shift(1) * 100
print(daiy_change)

# daily cumulative return

daily_cumulative  = daiy_change.cumsum()
print(daily_cumulative)

daily_cumulative.plot(figsize=(30,20))
plt.show()


rv = IBM_daily_percent_change.rolling(window=10).std()
print(rv)
