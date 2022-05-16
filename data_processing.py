import pandas as pd


class DataExtraction:
    DATASET_FILENAME = "./data/paintcontrol.xlsx"
    DATASET_SHEET_NAME = "paintcontrol"
    DATA_EXTRACTION_FILENAME = "./data/paintcontrol_extract.xlsx"
    DATA_RESULTS_FILENAME = "./data/paintcontrol_results.xlsx"

    def extract_data(self):
        df = pd.read_excel(self.DATASET_FILENAME, sheet_name=self.DATASET_SHEET_NAME)
        gn = df.groupby("Name")
        test_names = df["Name"].unique()  # a list with unique test names
        data = []
        for test in test_names:
            test_group = gn.get_group(test)
            # iterate through each cycle and count how many times the verdict was error
            for cycle in range(1, 326):
                verdict_sum = 0
                for t in test_group.itertuples():
                    if t.Cycle == cycle:
                        verdict_sum += t.Verdict
                # print("Test: {}, Cycle: {}, Verdict: {}".format(test, cycle, verdict_sum))
                data.append([test, cycle, verdict_sum])
        self._write_df_to_file(self.DATA_EXTRACTION_FILENAME, data, columns=['Test', 'Cycle', 'Verdict'])

    def second_processing(self):
        df = pd.read_excel(self.DATASET_FILENAME, sheet_name=self.DATASET_SHEET_NAME)
        gn = df.groupby("Name")
        test_names = df["Name"].unique()  # a list with unique test names
        data = []
        # iterate through each unique test case name
        for test in test_names:
            row = [test]
            test_group = gn.get_group(test)
            all_cycles_verdict = 0
            all_cycles_runs = 0
            for cycle in range(1, 326):
                verdict_sum = 0
                count = 0
                for t in test_group.itertuples():
                    if t.Cycle == cycle:
                        count += 1  # count the number of runs of the test case in the current cycle
                        verdict_sum += t.Verdict  # compute the sum of verdict for the current cycle
                if count > 0:
                    all_cycles_runs += 1  # count the number of unique cycles in which the test was run
                row.append(count)
                row.append(verdict_sum)
                all_cycles_verdict += verdict_sum  # compute the sum of all verdicts for all the cycles
            row.append(all_cycles_verdict)
            row.append(all_cycles_runs)
            data.append(row)
        self._write_df_to_file(self.DATA_RESULTS_FILENAME, data)

    def _write_df_to_file(self, file_name, data, columns=None):
        if columns is None:
            columns = ["Name"]
            for cycle in range(1, 326):
                columns.append("Cycle {}".format(cycle))
                columns.append("Verdict Cycle {}".format(cycle))
            columns.append("All Cycles Verdict")
            columns.append("Nr Cycles Run")
        ddf = pd.DataFrame(data, columns=columns)
        ddf.to_excel(file_name, sheet_name=self.DATASET_SHEET_NAME, index=False)
