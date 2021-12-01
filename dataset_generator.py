import sys
import argparse
from WidyaGST import preprocessing

parser = argparse.ArgumentParser()
parser.add_argument("--input_dir", type=str)
parser.add_argument("--output_dir", type=str)
parser.add_argument("--dev_set_num", default=5, type=float)
parser.add_argument("--test_set_num", default=5, type=float)

global args
args = parser.parse_args()

if __name__ == "__main__":

    """
    Input Path Structure
    └── input_dir/
        ├── speaker-1/
        |    ├── speaker-1-01.wav
        |    ├── speaker-1-02.wav
        |    ├── ....
        |    ├── speaker-1-XX.wav
        |    └── transcript.csv
        └── speaker-2/
             ├── speaker-2-01.wav
             ├── speaker-2-02.wav
             ├── ....
             ├── speaker-2-XX.wav
             └── transcript.csv


    Output Path Structure Result
    └── output_dir/
        ├── train/
        |    ├── text
        |    ├── wav.scp
        |    ├── utt2spk
        |    └── spk2utt
        ├── dev/
        |    ├── text
        |    ├── wav.scp
        |    ├── utt2spk
        |    └── spk2utt
        └── eval/
             ├── text
             ├── wav.scp
             ├── utt2spk
             └── spk2utt
    """

    input_dir = args.input_dir
    output_dir = args.output_dir
    dev_set_num = args.dev_set_num
    test_set_num = args.test_set_num

    datasetGenarator = preprocessing.DatasetGenerator(
        input_dir=input_dir,
        output_dir=output_dir,
        dev_set_num=dev_set_num,
        test_set_num=test_set_num,
    )

    datasetGenarator()
