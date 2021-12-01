import parser
import argparse
from WidyaGST.utils import TextCleanerIndonesia

parser = argparse.ArgumentParser()
parser.add_argument("--input_path", type=str)
parser.add_argument("--output_path", type=str)

global args
args = parser.parse_args()

if __name__ == "__main__":

    input_path = args.input_path
    output_path = args.output_path

    cleaner = TextCleanerIndonesia(
        input_path=input_path,
        clean_number_state=True,
        text_column_position=1,
        csv_header=False,
        kaldi_style_text=True,
    )

    cleaner()
