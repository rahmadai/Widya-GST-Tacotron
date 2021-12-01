#!/usr/bin/env bash

# Copyright (C) Widya Wicara, Inc - All Rights Reserved
# For internal use only
# Written by Ilham Fazri - Machine Learning Engineer, 2021


#Widya Resampling Audio Test
python widya_resampling_audio.py --audio_dir=test/test_audio_resample/input_dir --target_sr=22050 --output_dir=test/test_audio_resample/output_dir

#Widya Audio Format Checker Test
python widya_audio_checker.py --input_dir=test/test_audio_format_checker --sr_requirement=22050 --data_format_requirement=PCM16 --channels_requirement=mono

#Widya Audio Float to PCM16 Test
python widya_float_to_pcm16.py --input_dir=test/test_float2pcm/input --output_dir=test/test_float2pcm/output

#Widya Single Audio Denoiser Test
python test/test_denoiser/test.py

#Widya VAD Croping Single File Test
python test/test_vad_singlefile/test.py 

#Widya VAD Croping Multiple Files Test
python widya_vad_croping.py --input_dir=test/test_vad_multiplefiles/input_dir --output_dir=test/test_vad_multiplefiles/output_dir

#Widya Multiple Audio Denoiser Test
python widya_audio_denoiser.py --input_dir=test/test_denoiser_multiple/input_dir --output_dir=test/test_denoiser_multiple/output_dir

#Widya Dataset to Kaldi-Style Test
python widya_kaldi_style_dataset.py --input_dir=test/test_to_kaldi-style_converter/input --output_dir=test/test_to_kaldi-style_converter/output