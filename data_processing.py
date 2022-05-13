import pandas as pd


def extract_data():
    df = pd.read_excel("./data/paintcontrol.xlsx", sheet_name="paintcontrol")
    gn = df.groupby("Name")
    test_names = df["Name"].unique()  # a list with unique test names
    data = []
    for test in test_names:
        test_group = gn.get_group(test)
        # iterate through each cycle and count how many times the verdict was error
        for cycle in range(1, 325):
            verdict_sum = 0
            for t in test_group.itertuples():
                if t.Cycle == cycle:
                    verdict_sum += t.Verdict
            # print("Test: {}, Cycle: {}, Verdict: {}".format(test, cycle, verdict_sum))
            data.append([test, cycle, verdict_sum])
    ddf = pd.DataFrame(data, columns=['Test', 'Cycle', 'Verdict'])
    print(ddf)
