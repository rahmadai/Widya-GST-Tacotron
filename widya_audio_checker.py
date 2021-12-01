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
        description="check audio files inside directory based on requirement"
    )
    parser.add_argument(
        "--input_dir", type=str, default=None, help="path to your audio files directory"
    )
    parser.add_argument(
        "--sr_requirement", type=int, default=None, help="sampling rate requirement"
    )
    parser.add_argument(
        "--data_format_requirement",
        type=str,
        default=None,
        help="data format requirement [PCM16/Float32]",
    )
    parser.add_argument(
        "--channels_requirement", type=str, default=None, help="mono/stereo"
    )
    return parser


def main():

    args = get_parser().parse_args()
    wav_list = WidyaGST.utils.path.find_wav_files(args.input_dir)

    print("\n\nWidya Check Audio Files Requirements")
    print("Input Directory : {}\n".format(os.path.realpath(args.input_dir)))

    count_not_meet_requirement = 0

    for wav in wav_list:
        audio_meta = WidyaGST.core.audio.check_audio_info(
            os.path.join(args.input_dir, wav)
        )
        if (
            audio_meta["data_format"] != args.data_format_requirement
            or audio_meta["channels"] != args.channels_requirement
            or audio_meta["sampling_rate"] != args.sr_requirement
        ):
            print("\033[1;31;40m{} does not meet requirements!".format(wav))
            count_not_meet_requirement += 1
        else:
            print("\033[1;32;40m{} meet requirements!".format(wav))

    if count_not_meet_requirement == 0:
        print("\033[1;32;40m \n\nresult : all wav files meet requirements!".format(wav))

    else:
        print(
            "\033[1;31;40m \n\nresult : some files does not meet requirements!".format(
                wav
            )
        )


if __name__ == "__main__":
    main()
