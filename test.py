from WidyaGST import utils
enhancedList = utils.FindWAVFile("/home/hamz/Part Time/Widya-GST-Tacotron/example")
for wav in enhancedList:
    print("{}.wav".format(wav[:-13]))