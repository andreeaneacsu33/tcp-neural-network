import csv

from sklearn.metrics import accuracy_score, recall_score, precision_score, auc, roc_curve
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
import pandas as pd

pd.set_option('display.max_columns', 10)

DATA_RESULTS_FILENAME = "./data/paintcontrol_results.xls"
DATA_METRICS_FILENAME = "./data/paintcontrol_metrics.csv"

feature_length = 655
data = pd.read_excel(DATA_RESULTS_FILENAME)

features = data.iloc[:, :feature_length]
labels = data.iloc[:, feature_length]

alg_config = ['lbfgs', 'sgd', 'adam']
layers_config = [(10,), (10, 10), (10, 10, 10)]

datasets = train_test_split(features, labels, test_size=0.2)

train_data, test_data, train_labels, test_labels = datasets

with open(DATA_METRICS_FILENAME, 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    header = ['Solver', 'Layer', 'Accuracy Train', 'Accuracy Test', 'Precision Train', 'Precision Test',
              'Recall Train', 'Recall Test', 'AUC Train', 'AUC Test']
    writer.writerow(header)

    for solver in alg_config:
        for layer in layers_config:
            clf = MLPClassifier(solver=solver, alpha=1e-5, hidden_layer_sizes=layer, random_state=1, max_iter=500)

            clf.fit(train_data, train_labels)
            clf.score(test_data, test_labels)

            predictions_train = clf.predict(train_data)
            predictions_test = clf.predict(test_data)

            accuracy_train = accuracy_score(predictions_train, train_labels)
            accuracy_test = accuracy_score(predictions_test, test_labels)

            precision_train = precision_score(predictions_train, train_labels, average='macro')
            precision_test = precision_score(predictions_test, test_labels, average='macro')

            recall_train = recall_score(predictions_train, train_labels, average='macro', zero_division=0)
            recall_test = recall_score(predictions_test, test_labels, average='macro', zero_division=0)

            fpr_train, tpr_train, thresholds_train = roc_curve(train_labels, predictions_train, pos_label=2)
            auc_train = auc(fpr_train, tpr_train)

            fpr_test, tpr_test, thresholds_test = roc_curve(test_labels, predictions_test, pos_label=2)
            auc_test = auc(fpr_test, tpr_test)

            writer.writerow(
                [solver, layer, accuracy_train, accuracy_test, precision_train, precision_test, recall_train,
                 recall_test, auc_train, auc_test])

df = pd.read_csv(DATA_METRICS_FILENAME)
df.sort_values(["Accuracy Test"], axis=0, ascending=False, inplace=True, na_position='first')
print(df)
