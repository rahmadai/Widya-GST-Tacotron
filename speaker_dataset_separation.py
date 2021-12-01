import os
import re
import csv
import shutil
import numpy as np

from tqdm import tqdm
from WidyaGST import utils

OUTPUT_FOLDER = "/home/hamz/Part Time/GST-Speaker"
FOLDER_PATH = "/home/hamz/Part Time/GST-TTS From STT Clean"
DATASET_LIST = os.listdir(FOLDER_PATH)


def sort_filename_transcript(list_filename):
    index_sorted = np.argsort(list_filename)
    return index_sorted


if __name__ == "__main__":

    # Create list all of wav files
    all_filenames = []
    for dataset in DATASET_LIST:
        dataset_path = os.path.join(FOLDER_PATH, dataset)
        list_files = os.listdir(os.path.join(dataset_path, "audio"))
        all_filenames += list_files

    # Create list all of speakers
    list_speaker = []
    for wav in all_filenames:
        regex = r"[a-z0-9]+"
        x = re.findall(regex, wav)
        if (x[0] in list_speaker) == False:
            list_speaker.append(x[0])

    print(list_speaker)

    all_filenames = []
    all_transcript = []
    source_folder = []
    # CSV 001
    with open(
        "/home/hamz/Part Time/GST-TTS From STT Clean/001/001.csv", mode="r"
    ) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            row_data = row["path\tfilesize\tsentence"].split("\t")
            all_filenames.append(row_data[0])
            all_transcript.append(row_data[2])
            source_folder.append("001")

    # CSV 002
    with open(
        "/home/hamz/Part Time/GST-TTS From STT Clean/002/002.csv", mode="r"
    ) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            row_data = row["filename\tfilesize\ttranscript"].split("\t")
            all_filenames.append(row_data[0])
            all_transcript.append(row_data[2])
            source_folder.append("002")

    # CSV 003
    with open(
        "/home/hamz/Part Time/GST-TTS From STT Clean/003/003.csv", mode="r"
    ) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            row_data = row["filename|filesize|sentence"].split("|")
            all_filenames.append(row_data[0])
            all_transcript.append(row_data[2])
            source_folder.append("003")

    # CSV 004
    with open(
        "/home/hamz/Part Time/GST-TTS From STT Clean/004/004.csv", mode="r"
    ) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            row_data = row["\tfilename\tfilesize\ttranscript"].split("\t")
            all_filenames.append(row_data[1])
            all_transcript.append(row_data[3])
            source_folder.append("004")

    for speaker in list_speaker:
        print(speaker)
        speaker_output_path = os.path.join(OUTPUT_FOLDER, speaker)
        utils.CreateFolder(speaker_output_path)
        speaker_filenames = []
        speaker_transcript = []
        for i in tqdm(range(0, len(all_filenames))):
            regex = r"[a-z0-9]+"
            x = re.findall(regex, all_filenames[i])
            if speaker == x[0]:
                input_audio_path = os.path.join(FOLDER_PATH, source_folder[i])
                input_audio_path = os.path.join(input_audio_path, "audio")
                input_audio_path = os.path.join(input_audio_path, all_filenames[i])
                output_audio_path = os.path.join(speaker_output_path, all_filenames[i])
                shutil.copyfile(input_audio_path, output_audio_path)
                speaker_filenames.append(all_filenames[i])
                speaker_transcript.append(all_transcript[i])

        # Create CSV Transcript
        index_sorted = sort_filename_transcript(speaker_filenames)

        csv_path = os.path.join(speaker_output_path, "transcript.csv")
        with open(csv_path, "w", encoding="UTF8", newline="") as file:
            writer = csv.writer(file, delimiter="\t")
            writer.writerow(["filename", "transcript"])
            for j in range(0, len(index_sorted)):
                writer.writerow(
                    [
                        speaker_filenames[index_sorted[j]],
                        speaker_transcript[index_sorted[j]],
                    ]
                )
