from sklearn import tree
from joblib import dump, load
import numpy as np
import json

with open('inputs.json') as json_file:
    features = np.array(json.load(json_file))

with open('outputs.json') as json_file:
    labels = np.array(json.load(json_file))

for i in range(len(features)):
    features[i] = features[i][:+(260-len(features[i]))]
    print(len(features[i]))

clf = tree.DecisionTreeRegressor()
clf = clf.fit(list(features), list(labels))

dump(clf, '30M.joblib') 
#prediction = clf.predict([[avgtemp, snow, rain, maxwind, high, low]])

#result
#print(prediction)