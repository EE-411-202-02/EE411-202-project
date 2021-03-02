import numpy as np
import adi
import scipy.constants as con
import matplotlib
import matplotlib.pyplot as plt
import scipy
from scipy import signal
import control

matplotlib.use('TkAgg')

class digital_signal:
    def __init__(self):
        self.x = None       # The signal.
        self.N = None       # Signal length.
        self.n = None       # Sample number.
        self.fs = None      # Sampling frequency.
        self.X = None       # FFT of x.
        self.freq = None    # Frequency axis of X.
    def gen_n(self):
        self.n = np.arange(np.size(self.x))

    def plot_signal(self, fig):
        plt.figure(fig)
        plt.plot(self.n, self.x)
        plt.xlabel("n")
        plt.ylabel("X[n]")
        plt.show()

    def plot_fft(self, fig):
        self.X = scipy.fft.fft(self.x)
        self.freq = scipy.fft.fftfreq(np.size(self.X), d=1 / self.fs)
        plt.figure(fig)
        plt.semilogy(self.freq, np.abs(self.X))
        plt.xlabel('frequency [Hz]')
        plt.ylabel('P [dB]')
        plt.show()

    def gain(self, db):
        a = control.db2mag(db)
        self.x = self.x * a

    def mov_avg(self, N):
        self.x = np.convolve(self.x, np.ones(N) / N, mode='valid')
