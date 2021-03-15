# This script will take raw signal and process it

import numpy as np
from DSP_tools import digital_signal


class process:
    def __init__(self, x_raw):
        self.si = digital_signal()  # Use DSP_tools.py.
        self.sq = digital_signal()

        self.si.x = np.real(x_raw)  # Raw input signal.
        self.n0i = None             # Indices of tx signal.
        self.x_temp_i = None        # Full samples of one scan.
        self.max_noise_i = None     # Noise floor
        self.threshold = None       # Detection threshold.
        self.d = None               # Slot number with detected target.
        self.si.xs = None           # Synced signal.

    def filter(self, sample_per_step):
        # Apply moving average filter.
        # self.si.gain(-30)
        m0, m1 = max(self.si.x), max(-self.si.x)
        if m0 < m1:
            m = -m1
        else:
            m = m0
        self.si.x = self.si.x * (m / abs(m))
        self.si.mov_avg(sample_per_step)
        self.si.x = abs(self.si.x)

    def sync(self, samples_per_scan):
        # This function syncs the Rx to Tx.
        tx_lvl = max(self.si.x) - 0.5  # Tx signal level.
        # samples_per_scan:                     # Number of samples in one scan.
        self.n0i = np.where(self.si.x > tx_lvl)[0]
        x_temp = self.si.x[int(self.n0i[0]):self.n0i[0] + samples_per_scan]
        i = np.arange(int((np.size(x_temp)) / 2))
        temp = np.zeros(int((np.size(x_temp)) / 2))
        for n in i:
            temp[n] = np.max(x_temp[2 * n:2 * n + 1])

        self.si.x = temp

    def detect(self, threshold):
        self.d = np.where(self.si.x > threshold)[0]

    def get_threshold(self):
        self.si.histogram()
        self.si.h = self.si.h / np.size(self.si.x)
        c = 0
        for i in range(np.size(self.si.h)):
            c = c + self.si.h[int(i)]
            self.si.h[i] = c

        temp = np.where((self.si.h >= 0.99))[0]
        self.threshold = self.si.hb[temp[0]]
