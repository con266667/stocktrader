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
import json

symbol = 'F'

inputs = []
outputs = []

#Get Data
date = datetime.datetime(2019, 12, 6, 12, 00)
ts = TimeSeries(key='0C661NOI2HN9KMEP',output_format='json')
data, meta_data = ts.get_intraday(symbol=symbol,interval='1min', outputsize='full')

tsYear = TimeSeries(key='0C661NOI2HN9KMEP',output_format='json')
dataFull, meta_dataFull = tsYear.get_daily(symbol=symbol, outputsize='full')

dateYear = (date-timedelta(weeks=52)).strftime('%Y-%m-%d')
dateMonth = (date-timedelta(weeks=4)).strftime('%Y-%m-%d')
monthAgoPrice = dataFull[dateMonth]['4. close']
yearAgoPrice = dataFull[dateYear]['4. close']


#Get News Articles
datelist = []
newsapi = NewsApiClient(api_key='12c0dd1174cf42c9845f1b9355a3f91d')
articles = newsapi.get_everything(q=symbol)

def nearest(items, pivot):
    return min(items, key=lambda x: abs(x - pivot))

for i in range(len(articles['articles'])):
    datelist.append(datetime.datetime.strptime(articles['articles'][i]['publishedAt'], '%Y-%m-%dT%H:%M:%SZ'))

index = datelist.index(nearest(datelist, date))
recentArticle = articles['articles'][index]
recentArticleTitle = recentArticle['title']
recentArticleContent = recentArticle['content']
recentArticleDate = (datetime.datetime.strptime(recentArticle['publishedAt'], '%Y-%m-%dT%H:%M:%SZ')-date).days

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


clf = load('model.joblib') 

inputs = inputs[:+(260-len(inputs))]

prediction = clf.predict([inputs])

#result
print(prediction)

def test():
    afterDate = float(data[(date+timedelta(minutes=30)).strftime('%Y-%m-%d %H:%M:00')]['4. close'])
    print(((afterDate-atDate)/afterDate)*100)

test()