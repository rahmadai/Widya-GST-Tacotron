#!/usr/bin/env python
# encoding: utf-8

# Copyright (C) Widya Wicara, Inc - All Rights Reserved
# For internal use only
# Written by Ilham Fazri - Machine Learning Engineer, 2021

import sys
import os

repo_path = os.path.dirname(os.path.realpath("test.py"))
sys.path.append(repo_path)

import WidyaGST.core.vad


if __name__ == "__main__":
    vad = WidyaGST.core.vad.voice_activity_detection()

    vad.load_file("test/test_vad_singlefile/input_audio.wav")

    vad.write_to_wav("test/test_vad_singlefile/output_audio.wav")
