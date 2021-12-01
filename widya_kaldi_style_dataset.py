#!/usr/bin/env python
# encoding: utf-8

# Copyright (C) Widya Wicara, Inc - All Rights Reserved
# For internal use only
# Written by Ilham Fazri - Machine Learning Engineer, 2021

import os
import argparse
import WidyaGST.utils.path
import WidyaGST.core.kaldi
import subprocess

from tqdm import tqdm


def get_parser():
    parser = argparse.ArgumentParser(
        description="denoiser audio (remove noisy background))"
    )
    parser.add_argument(
        "--input_dir", default=None, type=str, help="path to your audio files directory"
    )
    parser.add_argument(
        "--output_dir", default=None, type=str, help="path to your output directory"
    )
    parser.add_argument(
        "--dev_set_num", default=5, type=int, help="number of validation set data"
    )
    parser.add_argument(
        "--test_set_num", default=5, type=int, help="number of test set data"
    )

    return parser

def main():
    args = get_parser().parse_args()
    WidyaGST.utils.path.create_folder(args.output_dir)
    datasetGenarator = WidyaGST.core.kaldi.DatasetGenerator(
        input_dir=args.input_dir,
        output_dir=args.output_dir,
        dev_set_num=args.dev_set_num,
        test_set_num=args.test_set_num,
    )
    datasetGenarator()

    #Fix Dev Folder
    bashCommand = [
        "./kaldi_utils/fix_data_dir.sh",
        "{}".format(os.path.join(args.output_dir, "dev"))
    ]

    process = subprocess.Popen(bashCommand, stdout=subprocess.PIPE)
    output, error = process.communicate()

    #dos2unix Text
    bashCommand = [
        "dos2unix",
        "{}".format(os.path.join(args.output_dir, "dev/text"))
    ]

    process = subprocess.Popen(bashCommand, stdout=subprocess.PIPE)
    output, error = process.communicate()

        #Fix Dev Folder
    bashCommand = [
        "./kaldi_utils/fix_data_dir.sh",
        "{}".format(os.path.join(args.output_dir, "eval"))
    ]

    process = subprocess.Popen(bashCommand, stdout=subprocess.PIPE)
    output, error = process.communicate()

    #dos2unix Text
    bashCommand = [
        "dos2unix",
        "{}".format(os.path.join(args.output_dir, "eval/text"))
    ]

    process = subprocess.Popen(bashCommand, stdout=subprocess.PIPE)
    output, error = process.communicate()

        #Fix Dev Folder
    bashCommand = [
        "./kaldi_utils/fix_data_dir.sh",
        "{}".format(os.path.join(args.output_dir, "train"))
    ]

    process = subprocess.Popen(bashCommand, stdout=subprocess.PIPE)
    output, error = process.communicate()

    #dos2unix Text
    bashCommand = [
        "dos2unix",
        "{}".format(os.path.join(args.output_dir, "train/text"))
    ]

    process = subprocess.Popen(bashCommand, stdout=subprocess.PIPE)
    output, error = process.communicate()
    

if __name__ == "__main__":
    main()