## Build a New Model

### Preprocessing
##### Audio Files Requirements
In building a new model, the first step that must be done is to make sure the audio files in  your dataset has following this requirement:

| Parameter              | Requirement   | Explanation     |
| :---                   |    :----:    |          ---: |
| Sample Rate     | 22050 Hz     | The script that we modified and has tested from espnet is <br /> using 22050 Hz. If you have the audio that doesn't meet the <br /> requirement you can resampling audio files in the next step
| Audio Data Format      | PCM16        | We used kaldi to extract X-Vector features such as MFCC. Kaldi <br/> only accepts data with audio data format PCM16. <br/> If your audio data format is float you can follow <br/>  this "Convert Float to PCM16" step in the next section |
| File Format            | WAV          | Kaldi & espnet use this format and also WAV files <br/> are uncompressed|
| Channels            | Mono          | Mono channels is enough for human voice |

If you are not sure data format on your audio files you can check data format with this script
- check audio data format
    ```sh
    $ cd Widya-GST-Tacotron
    $ python
    >>> import WidyaGST.core.audio
    >>> audio_path = your/audio/file.wav
    >>> metadata = WidyaGST.core.audio.check_audio_info(audio_path)
    >>> print(metadata)
    ```

To check all your audio files are meet the requirement above you can follow this script. You can also use this script for custom requirement, just change parameters based on your needs.
- to check whether all audio files inside directory meet the requirement
    ```sh
    $ cd Widya-GST-Tacotron
    $ python widya_audio_checker.py --input_dir=your/audio_files/directory --sr_requirement=22050 --data_format_requirement=PCM16 --channels_requirement=mono
    ```


#### Float32 to PCM16 (Optional)
If your audio data format in Float32 you can convert it to PCM16 using this script, it will reformat all of wav files inside "input_path" directory.

- Reformat audio files from Float32 to PCM16
    ```sh
    $ cd Widya-GST-Tacotron
    $ python widya_resampling_audio.py --input_dir=your/audio_files/directory  --output_dir=your/audio_files_output/directory 
    ```

#### Resampling Audio (Optional)
This step is optional only if your audio files isn't at 22050 Hz. Besides that you can use this script to upsampling or downsampling audio to any sample rate such as 16KHz, 24KHz, and 48KHz, to do that just change "target_sr" parameter. If you do upsampling into target sr that has a big difference with your audio files, We didn't guarantee the result of output audio files is good.

With this script, it will resample all of wav files inside "audio_dir" path.

- Resampling to 22050Hz
    ```sh
    $ cd Widya-GST-Tacotron
    $ python widya_resampling_audio.py --audio_dir=your/audio_files/directory --output_dir=your/audio_files_output/directory --target_sr=22050
    ```

### VAD & Denoiser (Optional)
The quality of the synthesized audio produced from text-to-speech (TTS) is influenced by the audio used in the training process. So if the audio quality used is bad then the text-to-speech model will also be bad. For example, bad audio quality is when there is so much noise in the background when the speaker speaking and there is a pause at the beginning or the end of the sound.

#### VAD Croping
With this script bellow the audio files will be cropped automatically based on voice activity detected, it also will remove pause at the beginning and the end of the sound. To hear before and after audio using this script click these links below.

[Before VAD Croping](https://drive.google.com/file/d/1_h7OcCBmVfONrENNt_1Qe_3Ff1Sa1jMr/view?usp=sharing) <br/>[After VAD Croping](https://drive.google.com/file/d/1nnQQ0_MkX2xGLr7Smdyo6nSuaabHGxaI/view?usp=sharingg)

- VAD croping single File
    ```sh
    $ cd Widya-GST-Tacotron
    $ python
    >>> import WidyaGST.core.vad
    >>> input_path = your/audio.wav
    >>> output_path = your/audio_output.wav
    >>> vad = WidyaGST.core.vad.voice_activity_detection()
    >>> vad.load_file(input_path)
    >>> vad.write_to_wav(output_path)

- VAD croping multiple files (inside directory)
    ```sh
    $ python widya_vad_croping.py --input_dir=audio/input_directory
    --output_dir=audio/output_directory

#### Denoiser
To reduce noisy background audio you can follow the script below. To hear the effect before and after audio using this denoiser you can click these links below. <br/>
[Before Denoiser](https://drive.google.com/file/d/1Lj6UnN01M332Z3HIo5HlQwtXbl20Becv/view?usp=sharing)
 <br/>
[After Denoiser](https://drive.google.com/file/d/1KuvSFgXv121y6wptLUdX9ZfJNuf_XJA_/view?usp=sharing)

- Denoiser single file
    ```sh
    $ cd Widya-GST-Tacotron
    $ python
    >>> import WidyaGST.core.audio
    >>> input_path = your/audio.wav
    >>> output_path = your/audio_output.wav
    >>> WidyaGST.core.audio.denoiser_single_audio(input_path, output_path)
    

- Denoiser multiple files
    ```sh
    $ cd Widya-GST-Tacotron
    $ python widya_audio_denoiser.py --input_dir=your/audio_files/directory --output_dir=your/audio_files_output/directory



### Dataset to Kaldi-style
We used espnet and kaldi-style datasets to training the model. So your dataset must follow a kaldi-style dataset structure. If you don't know about kaldi-style dataset structure you can check this link. It is so complicated if convert your dataset to kaldi-style in a manual way, so we created this script to make it easier and automatically in converting your dataset into a kaldi-style dataset. All you have to do is follow these steps below.

#### 1. Restructure Your Dataset
First you need to restructure your dataset files (audio files and transcript) into this directory tree structure format. 
"speaker_1" and "speaker_2" is represent speaker id you can change according to your needs for example "ani_21" or "toyib_45". 

- Dataset Directory Tree Structure
    ```sh
    dataset_gst/
    ├── speaker_1
    │   ├── speaker_1_1.wav
    │   ├── speaker_1_2.wav
    │   ├── speaker_1_3.wav
    │   ├── speaker_1_4.wav
    │   ├── ...
    │   ├── ...
    │   ├── speaker_1_n.wav
    │   └── transcript.csv
    ├── speaker_2
    │   ├── speaker_2_1.wav
    │   ├── speaker_2_2.wav
    │   ├── speaker_2_3.wav
    │   ├── speaker_2_4.wav
    │   ├── ...
    │   ├── ...
    │   ├── speaker_2_n.wav
    │   └── transcript.csv
    ├── ...
    |
    ├── ...
    |
    └── speaker_n
        ├── speaker_n_1.wav
        ├── speaker_n_2.wav
        ├── speaker_n_3.wav
        ├── speaker_n_4.wav
        ├── ...
        ├── ...
        ├── speaker_n_n.wav
        └── transcript.csv

#### 2. Transcript Format

As you can see each speaker id folder contains a transcript.csv file. That file contains the audio filenames and transcript texts for each speaker dataset. That transcript file must follow this format :
- "transcript.csv" Format
    ```sh
        cat speaker_1/transcript.csv 

        filename    transcript
        speaker_1_1.wav "Ibu pergi ke pasar"
        speaker_1_2.wav "Ayah pergi ke kantor"
        ...
        ...
        speaker_1_n.wav "Kakak pergi ke sekolah" 
    
#### 3. Convert to Kaldi-style
After you follow the structure format above you can follow this script to convert it your dataset into kaldi-style dataset format. 
- dataset to kaldi-style
    ```sh
        $ cd Widya-GST-Tacotron
        $ python widya_kaldi_style_dataset.py --input_dir=/dataset_path/dataset_gst --output_dir=dataset_path/output_kaldi

Directory tree structure of output folder will be like this.
- output folder
    ```sh
        output_kaldi/
        ├── dev
        │   ├── spk2utt
        │   ├── text
        │   ├── utt2spk
        │   └── wav.scp
        ├── eval
        │   ├── spk2utt
        │   ├── text
        │   ├── utt2spk
        │   └── wav.scp
        └── train
            ├── spk2utt
            ├── text
            ├── utt2spk
            └── wav.scp










