from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split, TunedThresholdClassifierCV
from sklearn.metrics import accuracy_score, confusion_matrix, make_scorer, recall_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_val_score

import pandas
import numpy

DATA = pandas.read_csv("DATA.csv")

DATA = pandas.DataFrame.dropna(DATA, axis = 0)
DATA = DATA[DATA.BPXDI2 > 10]
DATA = DATA[DATA.DIQ010 < 4]

DATA = DATA.drop("URXUMA", axis = 1)

DATA = DATA._get_numeric_data()
DATA = DATA.replace({"DIQ010": 3}, 1)
DATA = DATA.replace({"DIQ010": 2}, 0)

numpy_array = DATA.to_numpy()

pipe = make_pipeline(StandardScaler(), RandomForestClassifier(random_state = 0))

X = numpy_array[:, 1:7]
Y = numpy_array[:, 7]

X_TRAIN, X_TEST, Y_TRAIN, Y_TEST = train_test_split(X, Y, random_state=0)


pipe.fit(X_TRAIN, Y_TRAIN)
param_grid = {
   'randomforestclassifier__max_depth': [2, 4, 6, 8, 10],
   'randomforestclassifier__n_estimators': [5, 10, 15, 20, 25]}

search = GridSearchCV(pipe,
                            param_grid,
                            cv = 5)

search.fit(X_TRAIN, Y_TRAIN)

def cost_function(y, y_pred, neg_label, pos_label):
    cm = confusion_matrix(y, y_pred, labels = [neg_label, pos_label])
    cost_matrix = numpy.array([[0, -1], [-15, 0]])
    return numpy.sum(cm * cost_matrix)

cost_scorer = make_scorer(cost_function, neg_label = 0, pos_label = 1)

tuned_model = TunedThresholdClassifierCV(
    search,
    scoring = cost_scorer,
    store_cv_results = True)
tuned_model.fit(X_TRAIN, Y_TRAIN)
        
print(cost_scorer(search, X_TEST, Y_TEST))
print(cost_scorer(tuned_model, X_TEST, Y_TEST))

print(accuracy_score(tuned_model.predict(X_TEST), Y_TEST))

testing = pandas.DataFrame((tuned_model.predict(X_TEST)))

print(recall_score(Y_TEST, testing, average = "weighted"))
print(recall_score(Y_TEST, testing, pos_label = 0, average = "binary"))
scores = cross_val_score(tuned_model, X_TEST, Y_TEST, cv = 5)
print(scores.mean())
print(scores.std())