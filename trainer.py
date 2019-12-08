from sklearn import tree
from joblib import dump, load
import numpy as np
import json

with open('inputs1D.json') as json_file:
    features = json.load(json_file)

with open('outputs1D.json') as json_file:
    labels = json.load(json_file)

print(len(features))
deletes = []
for i in range(len(features)):
    if i < len(features):
        if len(features[i]) > 260:
            features[i] = features[i][:-(len(features[i])-260)]
        else:
            deletes.append(i)
        print("Length:"+str(len(features[i])))

for i in range(len(deletes)):
    features.remove(features[deletes[i]-i])
    labels.remove(labels[deletes[i]-i])

print(len(features))
print(len(labels))
clf = tree.DecisionTreeRegressor()
clf = clf.fit(list(features), list(labels))

dump(clf, '1D.joblib') 
#prediction = clf.predict([[avgtemp, snow, rain, maxwind, high, low]])

#result
#print(prediction)