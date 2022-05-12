import pandas as pd


def extract_data():
    df = pd.read_excel("./data/paintcontrol.xlsx", sheet_name="paintcontrol")
    gn = df.groupby("Name")
    test_names = df["Name"].unique()
    for test in test_names:
        test_group = gn.get_group(test)
        print(test_group)

