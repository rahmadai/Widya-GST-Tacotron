#!/usr/bin/env python
# encoding: utf-8

# Copyright (C) Widya Wicara, Inc - All Rights Reserved
# For internal use only
# Written by Ilham Fazri - Machine Learning Engineer, 2021

import WidyaGST.core.audio
import argparse
import os


def get_parser():
    parser = argparse.ArgumentParser(
        description="denoiser audio (remove noisy background))"
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

    print("\n\nWidya Audio Float to PCM16")
    print("Input Directory \t : {}".format(os.path.realpath(args.input_dir)))
    print("Output Directory \t : {}".format(os.path.realpath(args.output_dir)))

    WidyaGST.core.audio.denoiser_multiple_audio(args.input_dir, args.output_dir)


if __name__ == "__main__":
    main()
