import threading, queue, uuid, os
import numpy as np
import soundfile as sf
from pydub import AudioSegment

import matplotlib.pyplot as plt

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
    left_channel = data.T[0]
    right_channel = data.T[1]
    c = np.fft.fft(left_channel)
    # d = np.fft.fftfreq(7632495)
    # plt.plot(c.real)
    # plt.show()

    for block in sf.blocks(fp, blocksize=44100):
        left_ch = block.T[0]
        d = np.fft.fft(left_ch)
        freqs = np.fft.fftfreq(len(left_ch))
        plt.plot(d)
    plt.show()

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