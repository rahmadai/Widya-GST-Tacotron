import sys
import argparse
from WidyaGST import preprocessing

parser = argparse.ArgumentParser()
parser.add_argument("--input_path", type=str)
parser.add_argument("--output_path", type=str)
parser.add_argument("--active_denoiser", default=True, type=bool)
parser.add_argument("--save_audio_before_denoiser", default=False, type=bool)

global args
args = parser.parse_args()


if __name__ == "__main__":

    # Preprocessing Audio Files (Voice Activty Detection & Denoiser)
    inputPath = args.input_path
    outputPath = args.output_path
    active_denoiser = args.active_denoiser
    save_audio_before_denoiser = args.save_audio_before_denoiser

    audioPreprocessing = preprocessing.AudioPreprocessing(
        inputPath=inputPath,
        outputPath=outputPath,
        active_denoiser=active_denoiser,
        save_audio_before_denoiser=save_audio_before_denoiser,
    )
    audioPreprocessing()
