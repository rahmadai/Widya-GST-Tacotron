#!/usr/bin/env python
# encoding: utf-8

# Copyright (C) Widya Wicara, Inc - All Rights Reserved
# For internal use only
# Written by Ilham Fazri - Machine Learning Engineer, 2021

# Reference : https://github.com/pyannote/pyannote-audio

import torch
import soundfile as sf
from pyannote.audio.utils.signal import Binarize


class voice_activity_detection:
    def __init__(self):
        self.vad = torch.hub.load("pyannote/pyannote-audio", "sad_dihard")

    def load_file(self, audio_path):
        self.audio_path = audio_path
        self.start_duration, self.end_duration = self.detect_vad_timestamp()

    def detect_vad_timestamp(self):
        file_path = {"uri": "filename", "audio": "{}".format(self.audio_path)}

        vad_scores = self.vad(file_path)
        binarize = Binarize(
            offset=0.52,
            onset=0.52,
            log_scale=True,
            min_duration_off=0.1,
            min_duration_on=0.1,
        )

        result = binarize.apply(vad_scores, dimension=1)
        listSegment = result.for_json()["content"]

        startDuration = listSegment[0]["start"]
        endDuration = listSegment[-1]["end"]

        return startDuration, endDuration

    def write_to_wav(self, output_path):
        audio_data, sr = sf.read(self.audio_path)
        audio_vad = audio_data[
            int(self.start_duration * sr) : int(self.end_duration * sr)
        ]
        sf.write(output_path, audio_vad, sr, "PCM_16")
