from sklearn import tree
import datetime
from datetime import timedelta  
from alpha_vantage.timeseries import TimeSeries
import alpha_vantage
import matplotlib.pyplot as plt
from calendar import monthrange

symbol = 'TSLA'

#data['4. close'].plot()
#plt.title('Intraday TimeSeries')
#plt.show()
from newsapi import NewsApiClient

# Init
newsapi = NewsApiClient(api_key='12c0dd1174cf42c9845f1b9355a3f91d')

# /v2/top-headlines
articles = newsapi.get_everything(q=symbol)

# /v2/sources
sources = newsapi.get_sources()
date = datetime.datetime(2019, 12, 3, 9, 31)
ts = TimeSeries(key='0C661NOI2HN9KMEP',output_format='json')
data, meta_data = ts.get_intraday(symbol=symbol,interval='1min', outputsize='full')

tsYear = TimeSeries(key='0C661NOI2HN9KMEP',output_format='json')
dataYear, meta_dataYear = tsYear.get_monthly(symbol=symbol)
dateYear = (date-timedelta(weeks=52)).strftime('%Y-%m-')+str(monthrange(date.year, date.month)[1])
yearAgoPrice = dataYear[dateYear]['4. close']
print(yearAgoPrice)
minutesAfter = 24*60

def nearest(items, pivot):
    return min(items, key=lambda x: abs(datetime.datetime.strptime(x, '%Y-%m-%dT%H:%M:%SZ') - pivot))
datelist = []

for i in range(len(articles['articles'])):
    datelist.append(articles['articles'][i]['publishedAt'])

index = datelist.index(nearest(datelist, date))
recentArticle = articles['articles'][index]
atDate = float(data[date.strftime('%Y-%m-%d %H:%M:00')]['4. close'])
afterDate = float(data[(date+timedelta(minutes=minutesAfter)).strftime('%Y-%m-%d %H:%M:00')]['4. close'])
pandl = ((afterDate-atDate)/afterDate)*100
out = "P/L for {} - {}, range {}min = {}%".format(symbol, date, minutesAfter, pandl)
print(out)

#features = [[-3.6, 15.4, 0, 39, 0, -8], [-0.5, 13.8, 0, 52, 0, -7], [-15.8, 0, 0, 43, 0, -8], [-13.7, 0, 0, 37, 0, -7]]

#labels = [-5, 4, 7, -1]

#clf = tree.DecisionTreeClassifier()
#clf = clf.fit(features, labels)

#prediction = clf.predict([[avgtemp, snow, rain, maxwind, high, low]])

#result
#print(prediction)