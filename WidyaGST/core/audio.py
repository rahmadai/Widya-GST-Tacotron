#!/usr/bin/env python
# encoding: utf-8

# Copyright (C) Widya Wicara, Inc - All Rights Reserved
# For internal use only
# Written by Ilham Fazri - Machine Learning Engineer, 2021

import WidyaGST.utils.path
import scipy.io.wavfile
import scipy.signal
import numpy as np
import librosa
import audio_metadata
import soundfile as sf
import os
import subprocess

from librosa.core import audio


def resample(audio_path, output_path, target_sr):
    rate, data = scipy.io.wavfile.read(audio_path)
    resampling_factor = target_sr / rate

    samples = len(data) * resampling_factor
    rate_new = int(rate * resampling_factor)

    _ = scipy.signal.resample(data, int(samples))
    n = len(_)
    value = _[-1]
    __ = np.append(_, value)

    scipy.io.wavfile.write(output_path, rate_new, __)


def check_audio_info(audio_path):
    """
    To check audio data information such as samp
    """

    audio_meta = {}

    # check sr
    y, sr = librosa.load(audio_path, sr=None)
    audio_meta["sampling_rate"] = sr
    # Get audio metadata

    metadata = audio_metadata.load(audio_path)

    # check data format
    if str(metadata["streaminfo"]["audio_format"]) == "WAVEAudioFormat.PCM":
        audio_meta["data_format"] = "PCM16"
    elif str(metadata["streaminfo"]["audio_format"]) == "WAVEAudioFormat.IEEE_FLOAT":
        audio_meta["data_format"] = "Float32"

    # check mono/streo
    if str(metadata["streaminfo"]["channels"]) == "1":
        audio_meta["channels"] = "mono"
    else:
        audio_meta["channels"] = "stereo"

    return audio_meta


def float_to_pcm(input_path, output_path):
    """
    Convert audio files in Float32 to PCM16
    """
    y, sr = librosa.load(input_path, sr=None)

    sig = np.asarray(y)
    dtype = "int16"

    if sig.dtype.kind != "f":
        raise TypeError("'sig' must be a float array")

    i = np.iinfo(dtype)
    abs_max = 2 ** (i.bits - 1)
    offset = i.min + abs_max

    sig_pcm = (sig * abs_max + offset).clip(i.min, i.max).astype(dtype)

    sf.write(output_path, sig_pcm, sr, "PCM_16")


def denoiser_multiple_audio(input_dir, output_dir):
    """
    Denoiser multiple audio files
    """
    # Create output directory if didnt exist
    WidyaGST.utils.path.create_folder(output_dir)
    wav_list = WidyaGST.utils.path.find_wav_files(input_dir)

    # Get sampling rate audio
    _, sr = sf.read(os.path.join(input_dir, wav_list[0]))

    # Denoiser command using bash shell
    bashCommand = [
        "python",
        "-m",
        "denoiser.enhance",
        "--noisy_dir",
        "{}".format(input_dir),
        "--out_dir",
        "{}".format(output_dir),
        "--sample_rate",
        "{}".format(sr),
    ]

    process = subprocess.Popen(bashCommand, stdout=subprocess.PIPE)
    output, error = process.communicate()

    # Remove noisy files in output folder and rename files to original name
    wav_output_list = WidyaGST.utils.path.find_wav_files(output_dir)
    for wav in wav_output_list:
        if wav[-9:-4] == "noisy":
            WidyaGST.utils.path.remove_file(os.path.join(output_dir, wav))
        else:
            WidyaGST.utils.path.rename_file(
                os.path.join(output_dir, wav),
                os.path.join(output_dir, "{}.wav".format(wav[:-13])),
            )


def denoiser_single_audio(input_path, output_path):
    """
    Denoiser single audio files
    """
    basename = os.path.basename(input_path)
    input_audio_dir = os.path.dirname(input_path)
    temp_in_dir = os.path.join(input_audio_dir, "tmp")

    _, sr = sf.read(input_path)
    print(sr)

    WidyaGST.utils.path.create_folder(temp_in_dir)

    WidyaGST.utils.path.copy_file(input_path, os.path.join(temp_in_dir, basename))

    bashCommand = [
        "python",
        "-m",
        "denoiser.enhance",
        "--noisy_dir",
        "{}".format(temp_in_dir),
        "--out_dir",
        "{}".format(temp_in_dir),
        "--sample_rate",
        "{}".format(sr),
    ]

    process = subprocess.Popen(bashCommand, stdout=subprocess.PIPE)
    output, error = process.communicate()

    WidyaGST.utils.path.copy_file(
        "{}_{}.wav".format(os.path.join(temp_in_dir, basename[:-4]), "enhanced"),
        output_path,
    )
    WidyaGST.utils.path.delete_folder(temp_in_dir)
