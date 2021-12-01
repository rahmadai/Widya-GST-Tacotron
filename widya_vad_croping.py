#!/usr/bin/env python
# encoding: utf-8

# Copyright (C) Widya Wicara, Inc - All Rights Reserved
# For internal use only
# Written by Ilham Fazri - Machine Learning Engineer, 2021

import os
import argparse
import WidyaGST.core.vad
import WidyaGST.utils.path

from tqdm import tqdm


def get_parser():
    parser = argparse.ArgumentParser(
        description="vad audio croping (remove pause at the begining and the end of audio file)"
    )
    parser.add_argument(
        "--input_dir", type=str, default=None, help="path to your audio files directory"
    )
    parser.add_argument(
        "--output_dir", type=str, default=None, help="path to your output directory"
    )

    return parser


def main():

    args = get_parser().parse_args()
    wav_list = WidyaGST.utils.path.find_wav_files(args.input_dir)
    WidyaGST.utils.path.create_folder(args.output_dir)

    print("\n\nWidya VAD Croping Audio")
    print("Input Directory \t : {}".format(os.path.realpath(args.input_dir)))
    print("Output Directory \t : {}".format(os.path.realpath(args.output_dir)))

    vad = WidyaGST.core.vad.voice_activity_detection()
    for wav in tqdm(wav_list):
        vad.load_file(os.path.join(args.input_dir, wav))
        vad.write_to_wav(os.path.join(args.output_dir, wav))


if __name__ == "__main__":
    main()
