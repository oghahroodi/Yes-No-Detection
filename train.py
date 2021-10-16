from scipy.io import wavfile as wav
from scipy.fftpack import fft
from os import listdir
import pyaudio
import wave
import numpy as np
import matplotlib.pyplot as plt
import os

di = 'train/'
no = 0
cno = 0
yes = 0
cyes = 0
for i in range(300):
    s = 'no' + str(i) + '.wav'
    try:
        rate, tmp = wav.read(di + s)
        data = []
        for i in tmp:
            data.append(i[0])

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
        cno += 1
        if lowFreqRate > 0.7 and highFreqRate < 0.4 and freqEnergyUnder20000Rate > 0.8:
            no += 1

    except:
        os.system('sox ' + di + s + ' corrected/' + s)

for i in range(300):
    s = 'yes' + str(i) + '.wav'
    try:
        rate, tmp = wav.read(di + s)
        data = []
        for i in tmp:
            data.append(i[0])
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
        cyes += 1
        if not(lowFreqRate > 0.7 and highFreqRate < 0.4 and freqEnergyUnder20000Rate > 0.8):
            yes += 1
    except:
        os.system('sox ' + di + s + ' corrected/' + s)

print('YES acc : ', yes/cyes*100)
print('NO acc : ', no/cno*100)
