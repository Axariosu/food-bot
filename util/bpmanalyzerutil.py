import threading, queue, uuid, os
import numpy as np
import soundfile as sf
import math
from pydub import AudioSegment

import matplotlib.pyplot as plt
from scipy.signal import hilbert
from scipy.signal import convolve
from scipy.signal import fftconvolve
# https://pypi.org/project/SoundFile/0.8.1/
# https://pysoundfile.readthedocs.io/en/latest/
# SoundFile Documentation

# http://www.physics.utah.edu/~detar/lessons/python/numpy_fft/node3.html
# Plotting the result of a Fourier transform using Matplotlib's Pyplot

# http://sep.stanford.edu/data/media/public/sep/prof/waves.pdf
# FOURIER TRANSFORMS AND WAVES:
# in four long lectures

# https://github.com/jiaaro/pydub
# python ffmpeg port

# https://hgomersall.github.io/pyFFTW/
# pyFFTW is a pythonic wrapper around FFTW, the speedy FFT library

# https://stackoverflow.com/questions/3957025/what-does-a-audio-frame-contain
# .wav <data frame> information: 
# An audio frame, or sample, contains amplitude (loudness) information at that particular point in time. /
# To produce sound, tens of thousands of frames are played in sequence to produce frequencies.
# In the case of CD quality audio or uncompressed wave audio, there are around 44,100 frames/samples per second. /
# Each of those frames contains 16-bits of resolution, allowing for fairly precise representations of the sound levels. /
# Also, because CD audio is stereo, there is actually twice as much information, 16-bits for the left channel, 16-bits for the right.
# When you use the sound module in python to get a frame, it will be returned as a series of hexadecimal characters:
# One character for an 8-bit mono signal.
# Two characters for 8-bit stereo.
# Two characters for 16-bit mono.
# Four characters for 16-bit stereo.
# In order to convert and compare these values you'll have to first use the python wave module's functions to check the bit depth and number of channels. /
# Otherwise, you'll be comparing mismatched quality settings.

# https://www.audiolabs-erlangen.de/resources/MIR/2017-GI-Tutorial-Musik/2017_MuellerWeissBalke_GI_BeatTracking.pdf
# Tempo and Beat Tracking

# https://web.media.mit.edu/~tristan/Blog/WASPAA05_Tristan.pdf
# DOWNBEAT PREDICTION BY LISTENING AND LEARNING

# https://en.wikipedia.org/wiki/Rectifier#Full-wave_rectification
# Mathematically, this corresponds to the absolute value function.

# https://www.clear.rice.edu/elec301/Projects01/beat_sync/beatalgo.html
# Beat This
# A Beat Synchronization Project

queue = queue.Queue()

def converter(fp, queue):
    song = AudioSegment.from_mp3(f'{fp}')
    out_name = str(uuid.uuid4()) + ".wav"
    song.export(f'../{out_name}', format="wav")
    queue.put(out_name)

def mp3_to_wav(fp):
    """
    Given a filepath to an mp3 file:
    Returns a filename to the converted wav. 
    """
    thread = threading.Thread(target=converter, args=(fp, queue))
    thread.start()
    thread.join()
    return queue.get()

if __name__ == "__main__":
    # fp_to_wav = mp3_to_wav("../audio.mp3")
    
    fp = '../46537490-d263-43db-b01d-e1aeb094f627.wav'
    data, samplerate = sf.read(fp, always_2d=False)
    bandlimits = [0, 200, 400, 800, 1600, 3200]
    maxfreq = 4096
    left_channel = data.T[0]
    right_channel = data.T[1]
    dft = np.fft.fft(left_channel)
    n = dft.size
    nbands = len(bandlimits)

    bl, br = [], []
    for i in range(nbands - 1):
        bl.append(math.floor(bandlimits[i] / maxfreq * n / 2) + 1)
        br.append(math.floor(bandlimits[i + 1] / maxfreq * n / 2))

    bl.append(math.floor(bandlimits[nbands - 1]/maxfreq*n/2) + 1)
    br.append(math.floor(n/2))

    output = np.zeros(n)

    for i in range(nbands):
        output[bl[i]:br[i]] = dft[bl[i]:br[i]]
        output[n+1-br[i]:n+1-bl[i]] = dft[n+1-br[i]:n+1-bl[i]]
    print(output, output.shape)
    print(bl, br)
    # plt.plot(output)
    # plt.show()

    hannlen = round(.4 * 2 * maxfreq)
    hann = np.zeros(n)

    for i in range(hannlen):
        hann[i] = math.cos(i * math.pi / hannlen / 2) ** 2
    
    wave = np.fft.ifft(output)
    # for i in range(nbands):
    #     wave.append(np.fft.ifft(output[bl[i]:br[i]]).real)



    print(wave)
    plt.plot(wave)
    plt.show()








    # d = np.fft.fftfreq(len(left_channel))
    # plt.plot(d, c.real**2 + c.imag**2)
    # plt.show()
    # analytical_signal = hilbert(left_channel)
    # plt.plot(analytical_signal.real)
    # plt.plot(analytical_signal.imag)
    # amplitude_envelope = np.abs(analytical_signal)
    # plt.plot(amplitude_envelope)
    # plt.show()
    # plt.clf()
    # idx = 0
    # split_signals = []
    # for block in sf.blocks(fp, blocksize=44100):
    #     idx += 1
    #     if idx == 50:
    #         left_ch = block.T[0]
    #         d = np.fft.fft(left_ch)
    #         plt.plot(left_ch)
    #         plt.show()
    #         plt.clf()

    #         # freqs = np.fft.fftfreq(len(left_ch))
    #         for i in range(len(bands) - 1):
    #             # print(d[bands[i]:bands[i+1] - 1], bands[i], bands[i+1])
    #             # full_wave_rectified = np.absolute(d[bands[i]:bands[i+1]].real)
                
    #             # hanning_window = np.hanning(44100*0.4)
    #             # print(full_wave_rectified.shape, hanning_window.shape)
    #             # filter_pass = np.convolve(hanning_window, full_wave_rectified)
    #             # print(filter_pass.shape)
    #             # np.fft.ifft(filter_pass)
    #             # plt.plot(np.arange(bands[i], bands[i+1], 1), filter_pass)
    #             # plt.plot(filter_pass)
    #             k = d[bands[i]:bands[i+1]]
    #             split_signals.append(k)
    #             plt.plot(np.arange(bands[i], bands[i+1], 1), k)
    #             # np.fft.ifft(split_signal)
    #             # wave = hilbert(d[bands[i]:bands[i+1]].real)
    #             # plt.plot(np.arange(bands[i], bands[i+1], 1), wave)
                
    #         #     inverse_fft_d = np.fft.ifft(d[bands[i]:bands[i+1]])
    #         #     rectify_signal = np.absolute(inverse_fft_d)
    #         #     fft_rectify_signal = np.fft.fft(rectify_signal)
    #         #     plt.plot(np.arange(bands[i], bands[i+1], 1), fft_rectify_signal.real)

    #         # print(d.real.shape)
    #         # plt.plot(d.real)
    #     # plt.plot(freqs, d.real**2 + d.imag**2)
    # plt.show()
    # plt.clf()
    # # smoothing
    # wave = []
    # for i in range(len(split_signals)):
    #     print(split_signals[i].shape)
    #     ifft_signal = np.fft.ifft(split_signals[i])
    #     ifft_signal_absolute = np.absolute(ifft_signal)
    #     wave.append(ifft_signal)
    #     plt.plot(np.arange(bands[i], bands[i+1], 1), ifft_signal.real)
    # plt.show()
    # plt.clf()

    # freq = []
    # for i in range(len(wave)):
    #     frequency_to_add = np.fft.fft(wave[i])
    #     freq.append(frequency_to_add)
    #     plt.plot(frequency_to_add)
    # plt.show()
    # plt.clf()


    # k = np.concatenate(split_signals)
    # p = np.fft.ifft(k)
    # plt.plot(p)
    # plt.show()
    # plt.clf()


    # plt.clf()

    # for block in sf.blocks(fp, blocksize=44100):
    #     left_ch = block.T[0]
    #     d = np.fft.fft(left_ch)
    #     # freqs = np.fft.fftfreq(len(left_ch))
    #     # for i in range(len(bands) - 1):
    #     #     k = d[bands[i]:bands[i+1]]
    #     #     plt.plot(k.real)
    #     plt.plot(d.real[0:200])
    # plt.show()
    # # np.hsplit(data, 1)[0] first col of adata
    # # np.hsplit(data)
    # # print(data.max(), data.min())
    # # rms = [np.sqrt(np.mean(block**2)) for block in
    # #    sf.blocks(fp, blocksize=44100)]
    # for block in sf.blocks(fp, blocksize=44100):
    #     block_fft = np.fft.fft(block[:, 0])
    #     real_part = len(block_fft) / 2
    #     plt.plot(abs(block_fft[:, (real_part - 1)]), 'r')
    # plt.show()
        # print(np.fft.fft2(block))
        # print(np.hsplit(block, 1))
    # print(rms)
    # a = pyfftw.FFTW(data)
    # print(a)

    
    # print(rms, len(rms))
    # pyfftw.FFTW()
    # plt.plot(rms)
    # plt.show()
    # a = pyfftw.empty_aligned(128, dtype='complex128')
    # b = pyfftw.empty_aligned(128, dtype='complex128')
    # fft_object = pyfftw.FFTW(a, b)
    # c = pyfftw.empty_aligned(128, dtype='complex128')
    # ifft_object = pyfftw.FFTW(b, c, direction='FFTW_BACKWARD')
    # ar, ai = np.random.randn(2, 128)
    # a[:] = ar + 1j*ai

    # fft_a = fft_object()
    # print(fft_a)