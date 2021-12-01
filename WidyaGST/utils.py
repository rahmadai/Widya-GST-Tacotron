import os
import shutil
import csv
import re


def CreateFolder(path):
    dir = path
    check = os.path.isdir(dir)

    if not check:
        os.makedirs(dir)


def DeleteFolder(path):
    try:
        shutil.rmtree(path)
    except OSError as e:
        print("Error: %s : %s" % (path, e.strerror))


def RemoveFile(path):
    os.remove(path)


def FindWAVFile(path):
    listFile = os.listdir(path)
    listWAV = []
    for fileName in listFile:
        if fileName[-4:] == ".wav":
            listWAV.append(fileName)

    return listWAV


def RenameFile(oldName, newName):
    os.rename(oldName, newName)


class TextCleanerIndonesia:
    """
    TextCleanerIndonesia
    Documentation add soon!

    Todo:
    - Number Cleaning
        Satuan (Done), Puluhan , Ratusan, Ribuan, Nomor Telepon
    """

    def __init__(
        self,
        input_path,
        clean_number_state=True,
        text_column_position=1,
        csv_header=True,
        kaldi_style_text=False,
    ):
        self.clean_number_state = clean_number_state
        self.input_path = input_path
        self.text_column_position = text_column_position
        self.csv_header = csv_header
        self.kaldi_style_text = kaldi_style_text

    def __call__(self):
        self.load_file()

        if self.clean_number_state == True:
            self.number_cleaning()

    def load_file(self):

        with open(self.input_path, "r") as csv_file:
            csv_reader = csv.reader(csv_file)

            filename = []
            transcript = []

            # Check csv_file if has header skip it!
            if self.csv_header == True:
                print(next(csv_reader))

            for row in csv_reader:
                row_list_data = row[0].split(" ")

                if self.kaldi_style_text == True:
                    filename.append(row_list_data[0])
                    transcript.append(" ".join(row_list_data[1:]))
                else:
                    filename.append(row_list_data[0])
                    transcript.append(filename)

        self.filename = filename
        self.transcript = transcript

    def number_to_text(self, match):
        list_satuan_text = [
            "nol",
            "satu",
            "dua",
            "tiga",
            "empat",
            "lima",
            "enam",
            "tujuh",
            "delapan",
            "sembilan",
        ]
        match = match.group()

        num_text = ""
        print(match)

        if len(match) == 1:
            num_text = list_satuan_text[int(match)]

        if len(match) == 2:
            if int(match) == 11:
                num_text = "sebelas"
            elif int(match) == 10:
                num_text = "sepuluh"
            else:
                if int(match[0]) == 1:
                    num_text = "{} belas".format(list_satuan_text[int(match[1])])
                else:

                    if int(match[1]) == 0:
                        num_text = "{} puluh".format(list_satuan_text[int(match[0])])
                    else:
                        num_text = "{} puluh {}".format(
                            list_satuan_text[int(match[0])],
                            list_satuan_text[int(match[1])],
                        )
        print(num_text)
        return num_text

    def number_cleaning(self):
        # Regex Number Pattern
        number_pattern = r"[0-9]+"
        for self.index in range(0, len(self.transcript)):
            x = re.sub(number_pattern, self.number_to_text, self.transcript[self.index])
            print(x)
