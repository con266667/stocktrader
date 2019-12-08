from sklearn import tree
import datetime
from datetime import timedelta  
from alpha_vantage.timeseries import TimeSeries
import alpha_vantage
import matplotlib.pyplot as plt
from calendar import monthrange
from newsapi import NewsApiClient
from joblib import dump, load
import numpy as np
import time
import json

symbol = input('SYMBOL: ')
model = input('MODEL: ')
testMode = input('TESTMODE: ')
date = datetime.datetime
if testMode == "ON":
    year = input('YEAR: ')
    month = input('MONTH: ')
    day = input('DAY: ')
    hour = input('HOUR: ')
    minute = input('MINUTE: ')
    date = datetime.datetime(int(year),int(month),int(day),int(hour),int(minute))
else:
    date = datetime.datetime.now()

if model == '1D':
    clf = load('1D.joblib') 
elif model == '30M':
    clf = load('30M.joblib')
else:
    print('ERROR: Model Not Found')

def test():
    minutes = 0
    if model == '1D':
        minutes = 1440
    elif model == '30M':
        minutes = 30
    afterDate = float(data[(date+timedelta(minutes=minutes)).strftime('%Y-%m-%d %H:%M:00')]['4. close'])
    print(((afterDate-atDate)/afterDate)*100)

loop = True
while loop == True:
    inputs = []
    outputs = []

    #Get Data
    #date = datetime.datetime(2019, 12, 3, 12, 00)
    ts = TimeSeries(key='PHRW43NNN9JL62CC',output_format='json')
    data, meta_data = ts.get_intraday(symbol=symbol,interval='1min', outputsize='full')

    tsYear = TimeSeries(key='PHRW43NNN9JL62CC',output_format='json')
    dataFull, meta_dataFull = tsYear.get_daily(symbol=symbol, outputsize='full')

    dateYear = (date-timedelta(weeks=52)).strftime('%Y-%m-%d')
    dateMonth = (date-timedelta(weeks=4)).strftime('%Y-%m-%d')
    monthAgoPrice = dataFull[dateMonth]['4. close']
    yearAgoPrice = dataFull[dateYear]['4. close']


    #Get News Articles
    #datelist = []
    #newsapi = NewsApiClient(api_key='12c0dd1174cf42c9845f1b9355a3f91d')
    #articles = newsapi.get_everything(q=symbol)

    #def nearest(items, pivot):
    #    return min(items, key=lambda x: abs(x - pivot))

   #for i in range(len(articles['articles'])):
    #    datelist.append(datetime.datetime.strptime(articles['articles'][i]['publishedAt'], '%Y-%m-%dT%H:%M:%SZ'))

    #index = datelist.index(nearest(datelist, date))
    #recentArticle = articles['articles'][index]
    #recentArticleTitle = recentArticle['title']
    #recentArticleContent = recentArticle['content']
    #recentArticleDate = (datetime.datetime.strptime(recentArticle['publishedAt'], '%Y-%m-%dT%H:%M:%SZ')-date).days

    #Calculate Change
    atDate = float(data[date.strftime('%Y-%m-%d %H:%M:00')]['4. close'])
    volume = data[date.strftime('%Y-%m-%d %H:%M:00')]['5. volume']

    #Add Data
    #inputs.append(recentArticleTitle)
    #inputs.append(recentArticleContent)
    #inputs.append(recentArticleDate)
    inputs.append(atDate)
    inputs.append(int(volume))
    inputs.append(float(monthAgoPrice))
    inputs.append(float(yearAgoPrice))

    #Get Past Day
    dataDate = date
    pastDayClose = []
    pastDayVolume = []
    while dataDate.hour*60+dataDate.minute >= 571:
        dataDate = dataDate-timedelta(minutes=1)
        if dataDate.strftime('%Y-%m-%d %H:%M:00') in data:
            inputs.append(float(data[dataDate.strftime('%Y-%m-%d %H:%M:00')]['4. close']))
            inputs.append(float(data[dataDate.strftime('%Y-%m-%d %H:%M:00')]['5. volume']))

    deletes = []

    if inputs>=260:
        inputs = inputs[:-(len(inputs)-260)]
    else:
        print('ERROR: Not enough data')
    prediction = clf.predict([inputs])
    print(prediction)
    if testMode == "ON":
        test()
        loop = False
    else:
        time.sleep(30)

