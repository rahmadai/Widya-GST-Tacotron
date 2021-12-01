#!/usr/bin/env python
# encoding: utf-8

# Copyright (C) Widya Wicara, Inc - All Rights Reserved
# For internal use only
# Written by Ilham Fazri - Machine Learning Engineer, 2021

import os
import argparse
import WidyaGST.utils.path
import WidyaGST.core.audio

from tqdm import tqdm


def get_parser():
    parser = argparse.ArgumentParser(
        description="convert audio files in Float to PCM16 data format"
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
    print("\n\nWidya Audio Float to PCM16")
    print("Input Directory \t : {}".format(os.path.realpath(args.input_dir)))
    print("Output Directory \t : {}".format(os.path.realpath(args.output_dir)))

    WidyaGST.utils.path.create_folder(args.output_dir)

    for wav in tqdm(wav_list):
        WidyaGST.core.audio.float_to_pcm(
            input_path=os.path.join(args.input_dir, wav),
            output_path=os.path.join(args.output_dir, wav),
        )

    print(
        "\n{} audio files sucessful reformated from float to pcm16\n\n".format(
            len(wav_list)
        )
    )


if __name__ == "__main__":
    main()
