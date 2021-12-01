import sys
import os
import argparse
from WidyaGST import preprocessing
from WidyaGST import utils
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument("--audio_dir", type=str)
parser.add_argument("--output_dir", type=str)
parser.add_argument("--target_sr", type=int)

global args
args = parser.parse_args()


if __name__ == "__main__":

    audio_dir = args.audio_dir
    output_dir = args.output_dir
    target_sr = args.target_sr

    print("\nResample Audio to {} Hz".format(target_sr))

    list_folder = os.listdir(audio_dir)
    for folder in list_folder:
        print("Resample WAV files in folder {}".format(folder))
        audio_folder_path = os.path.join(audio_dir, folder)
        output_folder_path = os.path.join(output_dir, folder)
        utils.CreateFolder(output_folder_path)

        wav_list = utils.FindWAVFile(audio_folder_path)

        for wav in tqdm(wav_list):
            resample = preprocessing.Resample(
                audio_path=os.path.join(audio_folder_path, wav),
                target_sr=target_sr,
                output_path=os.path.join(output_folder_path, wav),
            )
            resample()
