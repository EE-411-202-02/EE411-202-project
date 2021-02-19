# This library contains functions used to interact with the SDR.

import numpy as np
import scipy.constants as con
import adi
import time

class SDR:
    def __init__(self):
        # Input:
        self.resolution = 0             # Range resolution in m.
        self.max_range = 0              # Maximum range in m.
        self.carrier_frequency = 0      # Carrier frequency in Hz.
        self.fsx = 0                    # Fs = fsx*2*pulseBW. *has to be supported by the ADC
        self.ip = "0.0.0.0"             # SDR IP
        self.tx_attenuation = 0         # Attenuation applied to Tx path (0dB to -90dB).
        self.num_pulses = 1             # Number of pulses per trigger.

        # Parameters:
        self.range_steps = 0            # Number of range steps.
        self.pulse_BW = 0               # Pulse bandwidth.
        self.pulse_width = 0            # Pulse width in s.
        self.sampling_frequency = 0     # Sampling frequency.
        self.repetition_frequency = 0   # Repetition frequency.
        self.num_samples = 0            # Number of samples to process.
        self.sdr = None                 # Empty adi object.
        self.tx_signal = 0              # Tx pulse.
        self.rx_signal = 0              # Rx signal.
        self.dwell_time = 0         # Dwell time in seconds.

    def calculate(self):
        # Calculate parameters:
        self.range_steps = int(self.max_range / self.resolution)
        prop_speed = con.speed_of_light
        self.pulse_BW = prop_speed / (2 * self.resolution)
        self.pulse_width = 1 / self.pulse_BW
        self.sampling_frequency = self.fsx * 2 * self.pulse_BW
        self.repetition_frequency = prop_speed/(2*self.max_range)
        self.num_samples = int((1 / self.repetition_frequency) * self.sampling_frequency + 2 * self.fsx)

        # Generate pulse:
        self.tx_signal = np.zeros(20)
        self.tx_signal[self.fsx:2 * self.fsx] = 2 ** 14  # samples are between -2^14 and +2^14

    def connect(self):
        self.sdr = adi.Pluto(self.ip)

    def send_setup(self):
        self.sdr.sample_rate = int(self.sampling_frequency)         # Send sampling rate (shared between Rx and Tx).
        self.sdr.tx_rf_bandwidth = int(self.sampling_frequency)     # Same as sampling rate.
        self.sdr.tx_lo = int(self.carrier_frequency)                # Tx local oscillator.
        self.sdr.tx_hardwaregain_chan0 = self.tx_attenuation        # Attenuation applied to Tx path.

        self.sdr.rx_rf_bandwidth = int(self.sampling_frequency/(2*self.fsx))    # Same as sampling rate.
        self.sdr.rx_lo = int(self.fsx)                                          # Rx local oscillator.
        self.sdr.gain_control_mode_chan0 = "manual"                             # Turn off AGC.
        self.sdr.rx_hardwaregain_chan0 = 0                                      # Rx gain.
        self.sdr.rx_buffer_size(self.num_samples)                               # Rx buffer size.

    def pulse(self):
        self.sdr.tx_destroy_buffer()        # Must be used to send a different signal.
        self.sdr.tx(self.tx_signal)         # Send the signal.
        time.sleep(self.dwell_time)     # Dwell time.
        self.rx_signal = self.sdr.rx()      # Pull Rx buffer.
