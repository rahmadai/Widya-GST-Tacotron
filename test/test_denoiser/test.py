#!/usr/bin/env python
# encoding: utf-8

# Copyright (C) Widya Wicara, Inc - All Rights Reserved
# For internal use only
# Written by Ilham Fazri - Machine Learning Engineer, 2021

import sys
import os

repo_path = os.path.dirname(os.path.realpath("test.py"))
sys.path.append(repo_path)


import WidyaGST.core.audio


if __name__ == "__main__":
    print("test")
    WidyaGST.core.audio.denoiser_single_audio(
        "test/test_denoiser/original_audio.wav", "test/test_denoiser/enhance_audio.wav"
    )
