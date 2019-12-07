from sklearn import tree
import datetime
from datetime import timedelta  
from alpha_vantage.timeseries import TimeSeries
import alpha_vantage
import matplotlib.pyplot as plt
from calendar import monthrange
from newsapi import NewsApiClient
import json

symbol = 'TSLA'
minutesAfter = 30

inputs = []
outputs = []

#Get Data
date = datetime.datetime(2019, 12, 5, 12, 00)
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
afterDate = float(data[(date+timedelta(minutes=minutesAfter)).strftime('%Y-%m-%d %H:%M:00')]['4. close'])
volume = data[(date+timedelta(minutes=minutesAfter)).strftime('%Y-%m-%d %H:%M:00')]['5. volume']
pandl = ((afterDate-atDate)/afterDate)*100
output = pandl
print(volume)
out = "P/L for {} - {}, range {}min = {}%".format(symbol, date, minutesAfter, pandl)
print(out)

#Add Data
inputs.append(recentArticleTitle)
inputs.append(recentArticleContent)
inputs.append(recentArticleDate)
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

append_to_json(inputs, 'inputs.json')
append_to_json(output, 'outputs.json')
#features = [[-3.6, 15.4, 0, 39, 0, -8], [-0.5, 13.8, 0, 52, 0, -7], [-15.8, 0, 0, 43, 0, -8], [-13.7, 0, 0, 37, 0, -7]]

#labels = [-5, 4, 7, -1]

#clf = tree.DecisionTreeClassifier()
#clf = clf.fit(features, labels)

#prediction = clf.predict([[avgtemp, snow, rain, maxwind, high, low]])

#result
#print(prediction)