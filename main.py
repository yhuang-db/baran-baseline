import argparse
import time

import toml
import raha
from raha import Detection, Correction

from eval import do_eval

if __name__ == "__main__":
    start = time.perf_counter()

    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--Toml")
    parser.add_argument("-c", "--Counter")
    args = parser.parse_args()
    toml_file = args.Toml
    counter = args.Counter
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
        exp_dataset.append({"name": dataset, "path": dirty_path, "clean_path": clean_path, "eval_attrs": dataset_dict["eval_attrs"]})

    for dataset_dictionary in exp_dataset:
        data = raha.dataset.Dataset(dataset_dictionary)

        # error detection
        app_detect = Detection()
        app_detect.VERBOSE = True
        app_detect.SAVE_RESULTS = False
        detection_dictionary = app_detect.run(dataset_dictionary)
        p, r, f = data.get_data_cleaning_evaluation(detection_dictionary)[:3]
        print("Raha's performance on {}:\nPrecision = {:.2f}\nRecall = {:.2f}\nF1 = {:.2f}".format(data.name, p, r, f))

        # error correction
        data.detected_cells = detection_dictionary
        app_correct = Correction()
        app_correct.VERBOSE = True
        app_correct.SAVE_RESULTS = False
        correction_dictionary = app_correct.run(data)
        p, r, f = data.get_data_cleaning_evaluation(correction_dictionary)[-3:]
        print("Baran's performance on {}:\nPrecision = {:.2f}\nRecall = {:.2f}\nF1 = {:.2f}".format(data.name, p, r, f))
        data.create_repaired_dataset(correction_dictionary=correction_dictionary)

        # attribute evaluation
        end = time.perf_counter()
        runtime = time.strftime("%Hh%Mm%Ss", time.gmtime(end - start))

        output_file = f'{dataset_dictionary["name"]}_eval_{counter}_{runtime}.csv'
        do_eval(data, dataset_dictionary["eval_attrs"], output_file)
