import argparse

import toml
import raha
from raha import Correction

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--Toml")
    args = parser.parse_args()
    toml_file = args.Toml
    print(toml_file)

    toml_dict = toml.load(toml_file)

    exp_dataset = []

    for dataset in toml_dict:
        dataset_dict = toml_dict[dataset]
        dir = dataset_dict["dir"]
        dirty_path = f"{dir}/{dataset}.csv"
        clean_path = f"{dir}/{dataset}_clean.csv"
        print(f"\n{dataset}")
        print(f"dirty path: {dirty_path}")
        print(f"clean path: {clean_path}")
        exp_dataset.append(
            {"name": dataset, "path": dirty_path, "clean_path": clean_path}
        )

    for dataset_dictionary in exp_dataset:
        data = raha.dataset.Dataset(dataset_dictionary)
        data.detected_cells = dict(data.get_actual_errors_dictionary())
        app = Correction()
        app.VERBOSE = True
        app.SAVE_RESULTS = False
        correction_dictionary = app.run(data)
        p, r, f = data.get_data_cleaning_evaluation(correction_dictionary)[-3:]
        print("Baran's performance on {}:\nPrecision = {:.2f}\nRecall = {:.2f}\nF1 = {:.2f}".format(data.name, p, r, f))
