import numpy as np
import scipy.constants as con


class TestSignal:
    def __init__(self):
        # Input:
        self.resolution = 0  # Range resolution in m.
        self.max_range = 0  # Maximum range in m.
        self.fc = 0  # Carrier frequency in Hz.
        self.fhs = 0                #
        self.fls = 0

        # Parameters:
        self.range_steps = None
        self.pulse_BW = None
        self.pulse_width = None
        self.t = None
        self.T = None

    def calculate(self):
        self.range_steps = int(self.max_range / self.resolution)    # Number of range steps.
        prop_speed = con.speed_of_light                             # Speed of light (m/s).
        self.pulse_BW = prop_speed / (2 * self.resolution)          # Pulse BW (Hz).
        self.pulse_width = 1 / self.pulse_BW                        # Pulse width (s).
        self.T = self.pulse_width * (self.range_steps + 2)          # Duration of the signal (s).
        self.hN = self.T * self.fhs                                 # Simulated signal duration.
        self.t = np.linspace(0, self.pulse_width * (self.range_steps + 2),)
    def