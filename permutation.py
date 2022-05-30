# best configs according to accuracy
# lbfgs (10, )
# sgd (10, )
# adam (10, )

import csv

import pandas as pd
from sklearn.neural_network import MLPClassifier

DATA_RESULTS_FILENAME = "data/paintcontrol_results.xls"
FILE_PERMUTATIONS_PREFIX = "./data/paintcontrol_results_{}.xlsx"
DATASET_SHEET_NAME = "paintcontrol"
DATA_PERMUTATIONS_FILENAME = "./data/paintcontrol_permutations.csv"

feature_length = 655

alg_config = ['lbfgs', 'sgd', 'adam']
layers_config = [(10,), (10,), (10,)]

permutations = []

for i in range(0, 3):
    data = pd.read_excel(DATA_RESULTS_FILENAME)

    features = data.iloc[:, :feature_length]
    labels = data.iloc[:, feature_length]

    clf = MLPClassifier(solver=alg_config[i], alpha=1e-5, hidden_layer_sizes=layers_config[i], random_state=1, max_iter=500)

    fit = clf.fit(features, labels)
    score = clf.score(features, labels)
    print("Score: ", score)

    prediction = clf.predict(features)

    data['Prediction'] = prediction

    data = data.sort_values(by='Prediction', ascending=False)
    data.to_excel(FILE_PERMUTATIONS_PREFIX.format(alg_config[i]), sheet_name=DATASET_SHEET_NAME, index=False)

    permutation = data['Name']

    permutations.append(permutation)


with open(DATA_PERMUTATIONS_FILENAME, 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    data = pd.read_excel(DATA_RESULTS_FILENAME)
    data = data.sort_values(by='Label', ascending=False)
    writer.writerow(['Initial', data['Name'].to_numpy()])
    for i in range(0, 3):
        writer.writerow([alg_config[i], permutations[i].to_numpy()])

