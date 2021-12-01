#!/usr/bin/env python
# encoding: utf-8

# Copyright (C) Widya Wicara, Inc - All Rights Reserved
# For internal use only
# Written by Ilham Fazri - Machine Learning Engineer, 2021

import sys
import os
import argparse
import WidyaGST.utils.path
import WidyaGST.core.audio

from tqdm import tqdm


def get_parser():
    parser = argparse.ArgumentParser(
        description="resampling audio file into any frequency sampling"
    )
    parser.add_argument(
        "--audio_dir", type=str, default=None, help="path to your audio files directory"
    )
    parser.add_argument(
        "--output_dir", type=str, default=None, help="path to your output directory"
    )
    parser.add_argument(
        "--target_sr", type=int, default=None, help="target sampling rate"
    )

    return parser


def main():

    args = get_parser().parse_args()

    wav_list = WidyaGST.utils.path.find_wav_files(args.audio_dir)
    print("\n\nWidya Resampling Audio")
    print("Input Directory \t : {}".format(os.path.realpath(args.audio_dir)))
    print("Output Directory \t : {}".format(os.path.realpath(args.output_dir)))
    print("\nResampling audio files to {} Hz".format(args.target_sr))

    WidyaGST.utils.path.create_folder(args.output_dir)

    for wav in tqdm(wav_list):
        resample = WidyaGST.core.audio.resample(
            audio_path=os.path.join(args.audio_dir, wav),
            target_sr=args.target_sr,
            output_path=os.path.join(args.output_dir, wav),
        )

    print(
        "{} audio files sucessful resampling to {}\n\n".format(
            len(wav_list), args.target_sr
        )
    )

if __name__ == "__main__":
    main()