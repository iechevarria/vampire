import argparse
import os
from shutil import copyfile
from typing import Optional

import pandas as pd


def split_data(dataframe: pd.DataFrame, n: int):
    other = dataframe.sample(n)
    dataframe = dataframe.drop(other.index)
    dataframe = dataframe.reset_index(drop=True)
    other = other.reset_index(drop=True)
    return dataframe, other


def run(data_dir: str, output_dir: str, split_dev: Optional[int] = None, split_test: Optional[int] = None, split_unlabeled: Optional[int] = None):
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    with open(os.path.join(data_dir, 'train.jsonl'), 'r') as file_:
        train = pd.read_json(file_, lines=True)
        orig_size = train.shape[0]

    if split_dev is not None:
        train, dev = split_data(train, split_dev)
        dev.to_json(os.path.join(output_dir, "dev.jsonl"), lines=True, orient='records')
    else:
        copyfile(os.path.join(data_dir, "dev.jsonl"),
                 os.path.join(output_dir, "dev.jsonl"))

    if split_unlabeled is not None:
        train, unlabeled = split_data(train, split_unlabeled)
        unlabeled.to_json(os.path.join(output_dir, "unlabeled.jsonl"), lines=True, orient='records')
    else:
        copyfile(os.path.join(data_dir, "unlabeled.jsonl"),
                 os.path.join(output_dir, "unlabeled.jsonl"))

    if split_test is not None:
        train, test = split_data(train, split_test)
        test.to_json(os.path.join(output_dir, "test.jsonl"), lines=True, orient='records')
    else:
        copyfile(os.path.join(data_dir, "test.jsonl"),
                 os.path.join(output_dir, "test.jsonl"))

    if train.shape[0] < orig_size:
        train.to_json(os.path.join(output_dir, "train.jsonl"), lines=True, orient='records')
    else:
        copyfile(os.path.join(data_dir, "train.jsonl"),
                 os.path.join(output_dir, "train.jsonl"))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()  # pylint: disable=invalid-name
    parser.add_argument('-d', '--data_dir', dest='data_dir', type=str, help='data directory', required=True)
    parser.add_argument('-o', '--output_dir', type=str, help='output directory', required=True)
    parser.add_argument('-x', '--split_dev', type=int, help='num of dev data', required=False)
    parser.add_argument('-t', '--split_test', type=int, help='num of test data', required=False)
    parser.add_argument('-u', '--split_unlabeled', type=int, help='num of unlabeled data', required=False)
    args = parser.parse_args()  # pylint: disable=invalid-name
    run(**args.__dict__)
    print(f"Complete. Split data located at {args.output_dir}")
