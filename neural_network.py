from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
import pandas as pd

DATA_RESULTS_FILENAME = "./data/paintcontrol_results.xlsx"

feature_length = 655
data = pd.read_excel(DATA_RESULTS_FILENAME)

data = data.iloc[:, :feature_length]
labels = data.iloc[:, feature_length]

clf = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(89, 1), random_state=1, max_iter=1000)

datasets = train_test_split(data,
                            labels,
                            test_size=0.2)

train_data, test_data, train_labels, test_labels = datasets

clf.fit(train_data, train_labels)
clf.score(train_data, train_labels)

predictions_train = clf.predict(train_data)
predictions_test = clf.predict(test_data)

train_score = accuracy_score(predictions_train, train_labels)
print("score on train data: ", train_score)
test_score = accuracy_score(predictions_test, test_labels)
print("score on test data: ", test_score)
