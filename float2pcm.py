import os
from tqdm import tqdm
import argparse
from WidyaGST import preprocessing
from WidyaGST import utils

parser = argparse.ArgumentParser()
parser.add_argument("--input_path", type=str)
parser.add_argument("--output_path", type=str)

global args
args = parser.parse_args()

if __name__ == "__main__":
    input_path = args.input_path
    output_path = args.output_path
    folder_list = os.listdir(input_path)
    for folder in folder_list:
        input_files_folder = os.path.join(input_path, folder)
        output_files_folder = os.path.join(output_path, folder)
        utils.CreateFolder(output_files_folder)

        files = utils.FindWAVFile(input_files_folder)
        print(folder)

        for file in tqdm(files):
            input_path_wav = os.path.join(input_files_folder, file)
            output_path_wav = os.path.join(output_files_folder, file)
            float2pcm = preprocessing.Float2PCM(input_path_wav, output_path_wav)
            float2pcm()

    # float2pcm = preprocessing.Float2PCM(input_path, output_path)
    # float2pcm()
