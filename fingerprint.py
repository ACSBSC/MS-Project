import librosa
import librosa.display
#from pydub import AudioSegment
import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import maximum_filter
import hashlib

def hashing(cmap, song_name):
    
    hashes = {}
    
    # Use this for binning - 45_000 is slighlty higher than the maximum
    # frequency rate of the given songs
    upper_frequency = 45_000 
    frequency_bits = 16
    
    time, frequency = np.argwhere(cmap == 1).T

    for idx1 in range(len(time)):
        for idx2 in range(idx1, idx1+10):
            if idx2>=len(time):
                break
            
            diff_time = time[idx2]-time[idx1]
            # If the time difference between the pairs is too small or large
            # ignore this set of pairs

            if diff_time <= 1 or diff_time > 10:
                continue

            #Place the frequencies (in Hz) into a 1024 bins
            freq_binned1 = frequency[idx1] / upper_frequency * (2 ** frequency_bits)
            freq_binned2 = frequency[idx2] / upper_frequency * (2 ** frequency_bits)
    
            # Produce a 32 bit hash
            # Use bit shifting to move the bits to the correct location
            
            hash = int(freq_binned1) | (int(freq_binned2) << 10) | (int(diff_time) << 20)
            hashes[hash] = (time[idx1], song_name)
    
    return hashes

def plot_constellation_map(Cmap, Y=None, xlim=None, ylim=None, title='',
                           xlabel='Time (sample)', ylabel='Frequency (bins)',
                           s=5, color='r', marker='o', figsize=(7, 3), dpi=72):
    if Cmap.ndim > 1:
        (K, N) = Cmap.shape
    else:
        K = Cmap.shape[0]
        N = 1
    if Y is None:
        Y = np.zeros((K, N))
    fig, ax = plt.subplots(1, 1, figsize=figsize, dpi=dpi)
    im = ax.imshow(Y, origin='lower', aspect='auto', cmap='gray_r', interpolation='nearest')
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    Fs = 1
    if xlim is None:
        xlim = [-0.5/Fs, (N-0.5)/Fs]
    if ylim is None:
        ylim = [-0.5/Fs, (K-0.5)/Fs]
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    n, k = np.argwhere(Cmap == 1).T
    ax.scatter(k, n, color=color, s=s, marker=marker)
    plt.tight_layout()
    return fig, ax, im

def compute_constellation_map(Y, dist_freq=7, dist_time=7, thresh=0.01):
    # spectrogram dimensions
    result = maximum_filter(Y, size=[2*dist_freq+1, 2*dist_time+1], mode='constant')
    Cmap = np.logical_and(Y == result, result > thresh)

    return Cmap

def compute_spectrogram(fn_wav, N=2048, H=1024, bin_max=128, frame_max=None):
    # sr == sampling rate 
    x, sr = librosa.load(fn_wav, sr=44100)
    x_duration = len(x)/sr
    # stft is short time fourier transform
    X = librosa.stft(x, n_fft=N, hop_length=H, win_length=N, window='hanning')
    if bin_max is None:
        bin_max = X.shape[0]
    if frame_max is None:
        frame_max = X.shape[0]
    Y = np.abs(X[:bin_max, :frame_max])
    
    '''# convert the slices to amplitude
    Xdb = librosa.amplitude_to_db(abs(X))

    # ... and plot, magic!
    plt.figure(figsize=(14, 5))
    librosa.display.specshow(Xdb, sr = sr, x_axis = 'time', y_axis = 'hz')
    plt.colorbar()
    plt.show()'''
    
    return Y

def fingerprint(filename):
    
    if '\\' in filename:
        song = filename.split("\\")
    else:
        song = filename.split("/")
    song=song[-1].split(".")
    #print(song)
    #song = song[1].split(".")
    song_name=song[-2]
    
    Y = compute_spectrogram(filename)

    dist_freq = 16  # kappa: neighborhood in frequency direction
    dist_time = 3   # tau: neighborhood in time direction
    
    for i in range(100):
        Cmap = compute_constellation_map(Y, dist_freq, dist_time)

    '''title=r'Constellation map using $\kappa=%d$, $\tau=%d$' % (dist_freq, dist_time)
    fig, ax, im = plot_constellation_map(Cmap, np.log(1 + 1 * Y), 
                                     color='r', s=30, title=title)
    plt.show()'''

    hashes = hashing(Cmap, song_name)
 
    return hashes