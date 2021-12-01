import numpy as np
import scipy.io.wavfile
import scipy.signal

if __name__ == "__main__":
    resampling_factor = 1.378125
    rate, data = scipy.io.wavfile.read("abd001_f_20201203_01_ayatalkitab1_ambon.wav")
    samples = len(data) * resampling_factor
    rate_new = int(rate * resampling_factor)
    print(rate_new)
    _ = scipy.signal.resample(data, int(samples))

    print(_)
    n = len(_)
    value = _[-1]
    __ = np.append(_, value)

    scipy.io.wavfile.write(
        "abd001_f_20201203_01_ayatalkitab1_ambon-resample.wav", rate_new, __
    )
