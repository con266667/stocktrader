from sklearn import tree
import datetime
from datetime import timedelta  
from alpha_vantage.timeseries import TimeSeries
import alpha_vantage
import matplotlib.pyplot as plt
from calendar import monthrange
from newsapi import NewsApiClient
from urllib import request
from bs4 import BeautifulSoup
import dateutil.relativedelta as dr
import pandas as pd
import json
import schedule
import time

#symbol = 'CPB'
minutesAfter = 60*24

tickers = []
ticker = 0

def get_constituents():
        # URL request, URL opener, read content
        req = request.Request('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
        opener = request.urlopen(req)
        content = opener.read().decode() # Convert bytes to UTF-8

        soup = BeautifulSoup(content)
        tables = soup.find_all('table') # HTML table we actually need is tables[0] 

        external_class = tables[0].findAll('a', {'class':'external text'})

        for ext in external_class:
            if not 'reports' in ext:
                tickers.append(ext.string)

get_constituents()

#Get Data
for ticker in range(len(tickers)):
    inputs = []
    outputs = []
    output = None
    append = True
    if '.' not in tickers[ticker+462] and ' ' not in tickers[ticker+462]:
        symbol = tickers[ticker+462]
    else:
        append = False

    date = datetime.datetime(2019, 12, 2, 12, 00)
    print(ticker+407)
    print(symbol)
    #symbol = 'TSLA'
    ts = TimeSeries(key='0C661NOI2HN9KMEP',output_format='json')
    data, meta_data = ts.get_intraday(symbol=symbol,interval='1min', outputsize='full')

    tsYear = TimeSeries(key='0C661NOI2HN9KMEP',output_format='json')
    dataFull, meta_dataFull = tsYear.get_daily(symbol=symbol, outputsize='full')

    dateYear = (date-timedelta(weeks=52)).strftime('%Y-%m-%d')
    dateMonth = (date-timedelta(weeks=4)).strftime('%Y-%m-%d')
    if dateMonth in dataFull and append == True:
        monthAgoPrice = dataFull[dateMonth]['4. close']
    else:
        append = False
        print("monthFalse")
    if dateYear in dataFull and append == True:
        yearAgoPrice = dataFull[dateYear]['4. close']
    else:
        append = False
        print("Yearfalse")

    #Calculate Change
    if date.strftime('%Y-%m-%d %H:%M:00') in data and append == True:
        atDate = float(data[date.strftime('%Y-%m-%d %H:%M:00')]['4. close'])
        volume = data[date.strftime('%Y-%m-%d %H:%M:00')]['5. volume']
    if (date+timedelta(minutes=minutesAfter)).strftime('%Y-%m-%d %H:%M:00') in data and append == True:
        afterDate = float(data[(date+timedelta(minutes=minutesAfter)).strftime('%Y-%m-%d %H:%M:00')]['4. close'])
    if (date+timedelta(minutes=minutesAfter)).strftime('%Y-%m-%d %H:%M:00') in data and date.strftime('%Y-%m-%d %H:%M:00') in data and append == True:
        pandl = ((afterDate-atDate)/afterDate)*100
        output = pandl
        print(volume)
        out = "P/L for {} - {}, range {}min = {}%".format(symbol, date, minutesAfter, pandl)
        print(out)
    else:
        append = False

    #Add Data
    #inputs.append(recentArticleTitle)
    #inputs.append(recentArticleContent)
    #inputs.append(recentArticleDate)
    if append == True:
        inputs.append(atDate)
        inputs.append(int(volume))
        inputs.append(float(monthAgoPrice))
        inputs.append(float(yearAgoPrice))

    #Get Past Day
    dataDate = date
    while dataDate.hour*60+dataDate.minute >= 571:
        dataDate = dataDate-timedelta(minutes=1)
        if dataDate.strftime('%Y-%m-%d %H:%M:00') in data:
            if append == True:
                inputs.append(float(data[dataDate.strftime('%Y-%m-%d %H:%M:00')]['4. close']))
                inputs.append(float(data[dataDate.strftime('%Y-%m-%d %H:%M:00')]['5. volume']))
    print(append)

    #Write Data
    def append_to_json(_dict,path): 
        with open(path, 'ab+') as f:
            f.seek(0,2)                                #Go to the end of file    
            if f.tell() == 0 :                         #Check if file is empty
                f.write(json.dumps([_dict]).encode())  #If empty, write an array
            else :
                f.seek(-1,2)           
                f.truncate()                           #Remove the last character, open the array
                f.write(' , '.encode())                #Write the separator
                f.write(json.dumps(_dict).encode())    #Dump the dictionary
                f.write(']'.encode())
    if append == True:
        with open('outputs1D.json') as json_file:
            outputsCheck = json.load(json_file)
        if output not in outputsCheck:
            append_to_json(inputs, 'inputs1D.json')
            append_to_json(output, 'outputs1D.json')
        else:
            print("Duplicate")
    time.sleep(30)
#features = [[-3.6, 15.4, 0, 39, 0, -8], [-0.5, 13.8, 0, 52, 0, -7], [-15.8, 0, 0, 43, 0, -8], [-13.7, 0, 0, 37, 0, -7]]

#labels = [-5, 4, 7, -1]

#clf = tree.DecisionTreeClassifier()
#clf = clf.fit(features, labels)

#prediction = clf.predict([[avgtemp, snow, rain, maxwind, high, low]])

#result
#print(prediction)