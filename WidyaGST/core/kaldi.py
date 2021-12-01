#!/usr/bin/env python
# encoding: utf-8

# Copyright (C) Widya Wicara, Inc - All Rights Reserved
# For internal use only
# Written by Ilham Fazri - Machine Learning Engineer, 2021

import WidyaGST.utils.path
import csv
import os


class DatasetGenerator:
    ### Dataset Generator for ESPnet2 TTS using Kaldi Style
    # https://github.com/espnet/espnet/tree/master/egs2/TEMPLATE#about-kaldi-style-data-directory

    def __init__(self, input_dir, output_dir, dev_set_num=5, test_set_num=5):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.dev_set_num = dev_set_num
        self.test_set_num = test_set_num

    def __call__(self):
        # Create output path
        output_train_dir = os.path.join(self.output_dir, "train")
        output_dev_dir = os.path.join(self.output_dir, "dev")
        output_eval_dir = os.path.join(self.output_dir, "eval")

        WidyaGST.utils.path.create_folder(output_train_dir)
        WidyaGST.utils.path.create_folder(output_dev_dir)
        WidyaGST.utils.path.create_folder(output_eval_dir)

        speakers_codefile_train = []
        speakers_filename_train = []
        speakers_transcript_train = []

        speakers_codefile_dev = []
        speakers_filename_dev = []
        speakers_transcript_dev = []

        speakers_codefile_eval = []
        speakers_filename_eval = []
        speakers_transcript_eval = []

        speakers_id = []

        list_speaker = os.listdir(self.input_dir)
        for speaker in list_speaker:
            speaker_codefile = []
            speaker_filename = []
            speaker_transcript = []
            csv_path = os.path.join(self.input_dir, speaker)
            csv_path = os.path.join(csv_path, "transcript.csv")
            with open(csv_path, mode="r") as csv_file:
                csv_data = csv.reader(csv_file)
                next(csv_data)
                for row in csv_data:
                    
                    data_row = row[0].split("\t")
                    speaker_codefile.append(data_row[0][:-4])
                    speaker_filename.append(data_row[0])
                    speaker_transcript.append(data_row[1])

            speakers_codefile_train.append(
                speaker_codefile[: -(self.dev_set_num + self.test_set_num)]
            )
            speakers_filename_train.append(
                speaker_filename[: -(self.dev_set_num + self.test_set_num)]
            )
            speakers_transcript_train.append(
                speaker_transcript[: -(self.dev_set_num + self.test_set_num)]
            )

            speakers_codefile_dev.append(
                speaker_codefile[
                    -(self.dev_set_num + self.test_set_num) : -(self.dev_set_num)
                ]
            )
            speakers_filename_dev.append(
                speaker_filename[
                    -(self.dev_set_num + self.test_set_num) : -(self.dev_set_num)
                ]
            )
            speakers_transcript_dev.append(
                speaker_transcript[
                    -(self.dev_set_num + self.test_set_num) : -(self.dev_set_num)
                ]
            )

            speakers_codefile_eval.append(speaker_codefile[-(self.dev_set_num) :])
            speakers_filename_eval.append(speaker_filename[-(self.dev_set_num) :])
            speakers_transcript_eval.append(speaker_transcript[-(self.dev_set_num) :])

            speakers_id.append(speaker)

        input_dir_realpath = os.path.realpath(self.input_dir)

        # Create wav.scp
        scp_train_path = os.path.join(output_train_dir, "wav.scp")
        with open(scp_train_path, mode="w") as scp_file:
            scp_writer = csv.writer(scp_file)
            for index in range(0, len(speakers_id)):
                for index_wav in range(0, len(speakers_codefile_train[index])):
                    file_path = os.path.join(input_dir_realpath, speakers_id[index])
                    file_path = os.path.join(
                        file_path, speakers_filename_train[index][index_wav]
                    )
                    scp_writer.writerow(
                        [
                            "{} {}".format(
                                speakers_codefile_train[index][index_wav], file_path
                            )
                        ]
                    )

        scp_dev_path = os.path.join(output_dev_dir, "wav.scp")
        with open(scp_dev_path, mode="w") as scp_file:
            scp_writer = csv.writer(scp_file)
            for index in range(0, len(speakers_id)):
                for index_wav in range(0, len(speakers_codefile_dev[index])):
                    file_path = os.path.join(input_dir_realpath, speakers_id[index])
                    file_path = os.path.join(
                        file_path, speakers_filename_dev[index][index_wav]
                    )
                    scp_writer.writerow(
                        [
                            "{} {}".format(
                                speakers_codefile_dev[index][index_wav], file_path
                            )
                        ]
                    )

        scp_eval_path = os.path.join(output_eval_dir, "wav.scp")
        with open(scp_eval_path, mode="w") as scp_file:
            scp_writer = csv.writer(scp_file)
            for index in range(0, len(speakers_id)):
                for index_wav in range(0, len(speakers_codefile_eval[index])):
                    file_path = os.path.join(input_dir_realpath, speakers_id[index])
                    file_path = os.path.join(
                        file_path, speakers_filename_eval[index][index_wav]
                    )
                    scp_writer.writerow(
                        [
                            "{} {}".format(
                                speakers_codefile_eval[index][index_wav], file_path
                            )
                        ]
                    )

        # Create text
        text_train_path = os.path.join(output_train_dir, "text")
        with open(text_train_path, mode="w") as text_file:
            text_writer = csv.writer(text_file)
            for index in range(0, len(speakers_id)):
                for index_wav in range(0, len(speakers_codefile_train[index])):
                    text_writer.writerow(
                        [
                            "{} {}".format(
                                speakers_codefile_train[index][index_wav],
                                speakers_transcript_train[index][index_wav],
                            )
                        ]
                    )

        text_dev_path = os.path.join(output_dev_dir, "text")
        with open(text_dev_path, mode="w") as text_file:
            text_writer = csv.writer(text_file)
            for index in range(0, len(speakers_id)):
                for index_wav in range(0, len(speakers_codefile_dev[index])):
                    text_writer.writerow(
                        [
                            "{} {}".format(
                                speakers_codefile_dev[index][index_wav],
                                speakers_transcript_dev[index][index_wav],
                            )
                        ]
                    )

        text_eval_path = os.path.join(output_eval_dir, "text")
        with open(text_eval_path, mode="w") as text_file:
            text_writer = csv.writer(text_file)
            for index in range(0, len(speakers_id)):
                for index_wav in range(0, len(speakers_codefile_eval[index])):
                    text_writer.writerow(
                        [
                            "{} {}".format(
                                speakers_codefile_eval[index][index_wav],
                                speakers_transcript_eval[index][index_wav],
                            )
                        ]
                    )

        # Create utt2spk
        utt2spk_train_path = os.path.join(output_train_dir, "utt2spk")
        with open(utt2spk_train_path, mode="w") as utt2spk_file:
            utt2spk_writer = csv.writer(utt2spk_file)
            for index in range(0, len(speakers_id)):
                for index_wav in range(0, len(speakers_codefile_train[index])):
                    utt2spk_writer.writerow(
                        [
                            "{} {}".format(
                                speakers_codefile_train[index][index_wav],
                                speakers_id[index],
                            )
                        ]
                    )

        utt2spk_eval_path = os.path.join(output_eval_dir, "utt2spk")
        with open(utt2spk_eval_path, mode="w") as utt2spk_file:
            utt2spk_writer = csv.writer(utt2spk_file)
            for index in range(0, len(speakers_id)):
                for index_wav in range(0, len(speakers_codefile_eval[index])):
                    utt2spk_writer.writerow(
                        [
                            "{} {}".format(
                                speakers_codefile_eval[index][index_wav],
                                speakers_id[index],
                            )
                        ]
                    )

        utt2spk_dev_path = os.path.join(output_dev_dir, "utt2spk")
        with open(utt2spk_dev_path, mode="w") as utt2spk_file:
            utt2spk_writer = csv.writer(utt2spk_file)
            for index in range(0, len(speakers_id)):
                for index_wav in range(0, len(speakers_codefile_dev[index])):
                    utt2spk_writer.writerow(
                        [
                            "{} {}".format(
                                speakers_codefile_dev[index][index_wav],
                                speakers_id[index],
                            )
                        ]
                    )
