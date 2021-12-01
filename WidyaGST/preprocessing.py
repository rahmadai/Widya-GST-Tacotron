import os
from posixpath import realpath
from numpy.core.arrayprint import dtype_short_repr
from tqdm import tqdm
import re
import torch
import soundfile as sf
import denoiser
import subprocess
import csv
import scipy.io.wavfile
import scipy.signal
import numpy as np
import librosa

from pyannote.audio.utils.signal import Binarize
from WidyaGST import utils


class AudioPreprocessing:

    def __init__(self, inputPath, outputPath, active_denoiser=False, save_audio_before_denoiser = False):
        self.inputPath = inputPath
        self.outputPath = outputPath
        self.active_denoiser = active_denoiser
        self.save_audio_before_denoiser = save_audio_before_denoiser

        try:
            self.vad = torch.hub.load('pyannote/pyannote-audio', 'sad_dihard')
            print("Load VAD Sucessfull")

        except:
            print("Failed to load VAD")


    def __call__(self):

        listWAV = utils.FindWAVFile(self.inputPath)
    
        for fileWAV in tqdm(listWAV):
            filePath = os.path.join(self.inputPath, fileWAV)
            startDuration, endDuration = self.detectVAD(filePath)
            audio, sr = self.audioCrop(startDuration, endDuration, filePath)

            outputDirTemp = os.path.join(self.outputPath, "tmp")
            utils.CreateFolder(outputDirTemp)
            outputPathWAV = os.path.join(outputDirTemp, fileWAV)
            sf.write(outputPathWAV, audio, sr, 'PCM_24')

        if(self.active_denoiser==True):    
            self.audioDenoiser(noisy_dir=outputDirTemp, out_dir=self.outputPath)
            enhancedList = utils.FindWAVFile(self.outputPath)

            for wav in enhancedList:

                 #Remove noisy files
                if(wav[-9:-4]=='noisy'):
                    utils.RemoveFile(os.path.join(self.outputPath, wav))
                
                #Rename enhanced file name to original file name
                else:
                    oldName = os.path.join(self.outputPath, wav)
                    newName = os.path.join(self.outputPath, "{}.wav".format(wav[:-13]))
                    utils.RenameFile(oldName, newName)
            
        if(self.save_audio_before_denoiser==False):
            utils.DeleteFolder(outputDirTemp)
        

    def detectVAD(self, path):
        file_path = {'uri':'filename','audio':'{}'.format(path)}
        vad_scores = self.vad(file_path)
        binarize = Binarize(offset=0.52, onset=0.52, log_scale=True, 
                    min_duration_off=0.1, min_duration_on=0.1)
        result = binarize.apply(vad_scores, dimension=1)
        listSegment = result.for_json()['content']

        startDuration = listSegment[0]['start']
        endDuration = listSegment[-1]['end']
        
        return startDuration, endDuration
    
    def audioCrop(self, startDuration, endDuration, path):
        audioFile, sr = sf.read(path)
        audioCrop = audioFile[int(startDuration*sr):int(endDuration*sr)]

        return audioCrop, sr

    def audioDenoiser(self, noisy_dir, out_dir):
        bashCommand = ["python", "-m", "denoiser.enhance", "--noisy_dir", 
        "{}".format(noisy_dir), "--out_dir","{}".format(out_dir)]
        process = subprocess.Popen(bashCommand, stdout=subprocess.PIPE)
        output, error = process.communicate()


class DatasetGenerator:
    ### Dataset Generator for ESPnet2 TTS using Kaldi Style
    #https://github.com/espnet/espnet/tree/master/egs2/TEMPLATE#about-kaldi-style-data-directory

    def __init__(self, input_dir, output_dir, dev_set_num = 5, test_set_num = 5):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.dev_set_num = dev_set_num
        self.test_set_num = test_set_num

    def __call__(self):
        #Create output path
        output_train_dir = os.path.join(self.output_dir, 'train')
        output_dev_dir = os.path.join(self.output_dir, 'dev')
        output_eval_dir = os.path.join(self.output_dir, 'eval')

        utils.CreateFolder(output_train_dir)
        utils.CreateFolder(output_dev_dir)
        utils.CreateFolder(output_eval_dir)
        
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
            csv_path = os.path.join(csv_path, 'transcript.csv')
            with open(csv_path, mode='r') as csv_file:
                csv_data = csv.reader(csv_file)
                next(csv_data)
                for row in csv_data:
                    data_row = row[0].split('\t')
                    speaker_codefile.append(data_row[0][:-4])
                    speaker_filename.append(data_row[0])
                    speaker_transcript.append(data_row[1])

            speakers_codefile_train.append(speaker_codefile[:-(self.dev_set_num+self.test_set_num)])
            speakers_filename_train.append(speaker_filename[:-(self.dev_set_num+self.test_set_num)])
            speakers_transcript_train.append(speaker_transcript[:-(self.dev_set_num+self.test_set_num)])

            speakers_codefile_dev.append(speaker_codefile[-(self.dev_set_num+self.test_set_num):-(self.dev_set_num)])
            speakers_filename_dev.append(speaker_filename[-(self.dev_set_num+self.test_set_num):-(self.dev_set_num)])
            speakers_transcript_dev.append(speaker_transcript[-(self.dev_set_num+self.test_set_num):-(self.dev_set_num)])

            speakers_codefile_eval.append(speaker_codefile[-(self.dev_set_num):])
            speakers_filename_eval.append(speaker_filename[-(self.dev_set_num):])
            speakers_transcript_eval.append(speaker_transcript[-(self.dev_set_num):])

            speakers_id.append(speaker)

        input_dir_realpath = os.path.realpath(self.input_dir)

        # Create wav.scp
        scp_train_path = os.path.join(output_train_dir, 'wav.scp')
        with open(scp_train_path, mode='w') as scp_file:
            scp_writer = csv.writer(scp_file)
            for index in range(0, len(speakers_id)):
                for index_wav in range(0, len(speakers_codefile_train[index])):
                    file_path = os.path.join(input_dir_realpath, speakers_id[index])
                    file_path = os.path.join(file_path, speakers_filename_train[index][index_wav])
                    scp_writer.writerow(["{} {}".format(speakers_codefile_train[index][index_wav], file_path)])

        scp_dev_path = os.path.join(output_dev_dir, 'wav.scp')
        with open(scp_dev_path, mode='w') as scp_file:
            scp_writer = csv.writer(scp_file)
            for index in range(0, len(speakers_id)):
                for index_wav in range(0, len(speakers_codefile_dev[index])):
                    file_path = os.path.join(input_dir_realpath, speakers_id[index])
                    file_path = os.path.join(file_path, speakers_filename_dev[index][index_wav])
                    scp_writer.writerow(["{} {}".format(speakers_codefile_dev[index][index_wav], file_path)])

        scp_eval_path = os.path.join(output_eval_dir, 'wav.scp')
        with open(scp_eval_path, mode='w') as scp_file:
            scp_writer = csv.writer(scp_file)
            for index in range(0, len(speakers_id)):
                for index_wav in range(0, len(speakers_codefile_eval[index])):
                    file_path = os.path.join(input_dir_realpath, speakers_id[index])
                    file_path = os.path.join(file_path, speakers_filename_eval[index][index_wav])
                    scp_writer.writerow(["{} {}".format(speakers_codefile_eval[index][index_wav], file_path)])

        # Create text
        text_train_path = os.path.join(output_train_dir, 'text')
        with open(text_train_path, mode='w') as text_file:
            text_writer = csv.writer(text_file)
            for index in range(0, len(speakers_id)):
                for index_wav in range(0, len(speakers_codefile_train[index])):
                    text_writer.writerow(["{} {}".format(speakers_codefile_train[index][index_wav], speakers_transcript_train[index][index_wav])])

        text_dev_path = os.path.join(output_dev_dir, 'text')
        with open(text_dev_path, mode='w') as text_file:
            text_writer = csv.writer(text_file)
            for index in range(0, len(speakers_id)):
                for index_wav in range(0, len(speakers_codefile_dev[index])):
                    text_writer.writerow(["{} {}".format(speakers_codefile_dev[index][index_wav], speakers_transcript_dev[index][index_wav])])
        
        text_eval_path = os.path.join(output_eval_dir, 'text')
        with open(text_eval_path, mode='w') as text_file:
            text_writer = csv.writer(text_file)
            for index in range(0, len(speakers_id)):
                for index_wav in range(0, len(speakers_codefile_eval[index])):
                    text_writer.writerow(["{} {}".format(speakers_codefile_eval[index][index_wav], speakers_transcript_eval[index][index_wav])])

        # Create utt2spk
        utt2spk_train_path = os.path.join(output_train_dir, 'utt2spk')
        with open(utt2spk_train_path, mode='w') as utt2spk_file:
            utt2spk_writer = csv.writer(utt2spk_file)
            for index in range(0, len(speakers_id)):
                for index_wav in range(0, len(speakers_codefile_train[index])):
                    utt2spk_writer.writerow(["{} {}".format(speakers_codefile_train[index][index_wav], speakers_id[index])])
        
        utt2spk_eval_path = os.path.join(output_eval_dir, 'utt2spk')
        with open(utt2spk_eval_path, mode='w') as utt2spk_file:
            utt2spk_writer = csv.writer(utt2spk_file)
            for index in range(0, len(speakers_id)):
                for index_wav in range(0, len(speakers_codefile_eval[index])):
                    utt2spk_writer.writerow(["{} {}".format(speakers_codefile_eval[index][index_wav], speakers_id[index])])
        
        utt2spk_dev_path = os.path.join(output_dev_dir, 'utt2spk')
        with open(utt2spk_dev_path, mode='w') as utt2spk_file:
            utt2spk_writer = csv.writer(utt2spk_file)
            for index in range(0, len(speakers_id)):
                for index_wav in range(0, len(speakers_codefile_dev[index])):
                    utt2spk_writer.writerow(["{} {}".format(speakers_codefile_dev[index][index_wav], speakers_id[index])])   

class Resample:
    def __init__(self, audio_path, target_sr, output_path):
        self.audio_path = audio_path
        self.target_sr = target_sr
        self.output_path = output_path
    
    def __call__(self):

        rate, data = scipy.io.wavfile.read(self.audio_path)
        resampling_factor = self.target_sr/rate

        samples = len(data) * resampling_factor
        rate_new = int(rate * resampling_factor)

        _ = scipy.signal.resample(data, int(samples))
        n = len(_)
        value = _[-1]
        __ = np.append(_, value)

        scipy.io.wavfile.write(self.output_path, rate_new, __)

class Float2PCM:
    """some code borrowed from https://github.com/mgeier/python-audio/blob/master/audio-files/utility.py"""

    def __init__(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path
    
    def __call__(self):
        y, sr = librosa.load(self.input_path, sr=None)
        sig = np.asarray(y)
        dtype =  'int16'


        if sig.dtype.kind != 'f':
            raise TypeError("'sig' must be a float array")
        
        i = np.iinfo(dtype)
        abs_max = 2**(i.bits - 1)
        offset = i.min + abs_max
        
        sig_pcm = ((sig * abs_max + offset).clip(i.min, i.max).astype(dtype))
        
        sf.write(self.output_path, sig_pcm, sr, 'PCM_16')


        
        




        

                
        
        

    
