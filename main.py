from scipy.io import wavfile as wav
from scipy.fftpack import fft
import pyaudio
import wave
import numpy as np
import matplotlib.pyplot as plt


# audio config params
FORMAT = pyaudio.paInt16  # format of sampling 16 bit int
CHANNELS = 1  # number of channels it means number of sample in every sampling
RATE = 44100  # number of sample in 1 second sampling
CHUNK = 1024  # length of every chunk
RECORD_SECONDS = 1.5  # time of recording in seconds
WAVE_OUTPUT_FILENAME = "file.wav"  # file name


audio = pyaudio.PyAudio()

print("recording...")
while True:
    # start Recording
    stream = audio.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK
    )

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    # print("finished recording")

    # stop Recording
    stream.stop_stream()
    stream.close()

    # storing voice
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

    # reading voice
    rate, data = wav.read('file.wav')
    # data is voice signal. its type is list(or numpy array)

    # find fourier transform of data
    f = np.fft.fft(data)
    m = np.absolute(f)
    m = m[0:int(len(m)/2)]
    p = np.angle(f)
    p = p[0:int(len(p)/2)]
    highFreqEnergy = 0
    freqEnergyUnder20000 = 0
    freqEnergyBelow20000 = 0
    lowFreqEnergy = 0
    energy = np.sum(m)

    for i in range(len(m)):
        if i < 4000:
            lowFreqEnergy += m[i]
        else:
            highFreqEnergy += m[i]
        if i < 20000:
            freqEnergyUnder20000 += m[i]
        else:
            freqEnergyBelow20000 += m[i]

    highFreqRate = highFreqEnergy/energy
    lowFreqRate = lowFreqEnergy/energy
    freqEnergyUnder20000Rate = freqEnergyUnder20000/energy
    freqEnergyBelow20000Rate = freqEnergyBelow20000/energy

    # print(highFreqRate)
    # print(lowFreqRate)
    # print(freqEnergyUnder20000Rate)
    # print(freqEnergyBelow20000Rate)

    if lowFreqRate > 0.7 and highFreqRate < 0.4 and freqEnergyUnder20000Rate > 0.8:
        print('NO')
    # elif 0.8 > highFreqRate > 0.4 and freqEnergyUnder20000Rate > 0.8 and 0.65 > lowFreqRate > 0.2:
    #     print('MUTE')
    # else:
    #     print('YES')
    # elif highFreqRate > 0.4 and lowFreqRate < 0.4 and freqEnergyUnder20000Rate > 0.7:
    #     print('YES')
    # else:
    #     print('MUTE')
    elif abs(freqEnergyUnder20000Rate-freqEnergyBelow20000Rate) < 0.9:
        print('MUTE')
    else:
        print('YES')

    print('-----------')

    # plt.plot(m)
    # plt.show()


audio.close()
