import cv2 as cv
import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd

'''os.chdir('Color+depth-20220317T010951Z-001/Color+depth/')
cwd = os.getcwd()
onlyfiles = os.listdir('.')[6:]
holstein =[]
count = 0
def accumulate(l):
    it = itertools.groupby(l, operator.itemgetter(0))
    for key, subiter in it:
       yield key, sum(item[1] for item in subiter) 

for file in onlyfiles[::4]:
    src = cv.imread(file)
    hsv = cv.cvtColor(src, cv.COLOR_BGR2HSV)
    holstein.append((hsv[240,320,:]))

#centers = list(accumulate(listy))
hdf = pd.DataFrame(holstein)
hdf['y'] = 0

os.chdir('C:/Users/indes/PycharmProjects/VT_Animal_SCI_ISE/RealsenseCameraTriggers/cows-20220318T181055Z-001/cows/')
onlyfiles1 = os.listdir('.')
print(onlyfiles1)
jersey = [] 
for file in onlyfiles1: 
    cv.imread(file)
    hsv = cv.cvtColor(src, cv.COLOR_BGR2HSV)
    jersey.append((hsv[240,320,:]))




jdf = pd.DataFrame(jersey)
jdf['y'] = 1



full_data_set = hdf.append(jdf)
full_data_set = full_data_set.reset_index()
print(full_data_set)
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

X_train, X_test, y_train, y_test = train_test_split(full_data_set[[0,1,2]], full_data_set['y'], test_size=0.2, random_state=0)
logreg = LogisticRegression()
logreg.fit(X_train, y_train)

y_pred = logreg.predict(X_test)
print('Accuracy of logistic regression classifier on test set: {:.2f}'.format(logreg.score(X_test, y_test)))

from sklearn.metrics import confusion_matrix
confusion_matrix = confusion_matrix(y_test, y_pred)
print(confusion_matrix)

from sklearn.metrics import classification_report
print(classification_report(y_test, y_pred))

os.chdir('C:/Users/indes/PycharmProjects/VT_Animal_SCI_ISE/RealsenseCameraTriggers/')'''





import pickle
#with open('cow_breed_identifier.pickle', 'wb') as f:
#    pickle.dump(logreg, f)


def cow_breed_classification(img)->bool: # in the form of an int
    # Change the image to a color matrix 
    print(img)
    src = cv.imread(img)
    hsv = cv.cvtColor(src, cv.COLOR_BGR2HSV)
    data = pd.DataFrame(hsv[240,320,:])
    print(data.T)
    # Load Trained model
    with open('Models/cow_breed_identifier.pickle', 'rb') as f:
        bClassifier = pickle.load(f)

    return bClassifier.predict(data.T)

def cow_weight_estimation(df)->int:#weight
    with open('Models/weight_estimation.pickle','rb') as f: 
        weight_predicter =pickle.load(f)
    return weight_predicter.predict(df)



