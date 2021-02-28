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
        self.dwell_time = 0             # Dwell time in seconds.
        self.sample_per_step = None     # Number of samples per step.
        self.tx_pulse = None            # Pulse shape.
        self.rx_buffer_size = None      # Rx buffer size.

    def calculate(self):
        # Calculate parameters:
        self.range_steps = int(self.max_range / self.resolution)            # Number of range steps.
        prop_speed = con.speed_of_light                                     # Speed of light (m/s).
        self.pulse_BW = prop_speed / (2 * self.resolution)                  # Pulse BW (Hz).
        self.pulse_width = 1 / self.pulse_BW                                # Pulse width (s).
        self.sampling_frequency = self.fsx * 2 * self.pulse_BW              # Sampling frequency (Hz).
        self.repetition_frequency = prop_speed/(2*self.max_range)           # Maximum repetition frequency.
        self.dwell_time = 1/self.repetition_frequency                       # Time per scan in one direction (s).
        self.num_samples = int(self.dwell_time * self.sampling_frequency)   # Number of useful samples.
        self.sample_per_step = int(self.num_samples / self.range_steps)     # Number of samples per step.
        self.rx_buffer_size = self.num_samples + 2 * self.sample_per_step   # size of the Rx buffer.

        # Generate pulse:
        self.tx_pulse = np.zeros(3*self.sample_per_step)
        self.tx_pulse[self.sample_per_step:2*self.sample_per_step] = np.ones(self.sample_per_step)
        self.tx_pulse = self.tx_pulse * (2**14)

    def connect(self):
        self.sdr = adi.Pluto(self.ip)

    def send_setup(self):
        self.sdr.sample_rate = int(self.sampling_frequency)         # Send sampling rate (shared between Rx and Tx).
        self.sdr.tx_rf_bandwidth = int(self.sampling_frequency)     # Same as sampling rate.
        self.sdr.tx_lo = int(self.carrier_frequency)                # Tx local oscillator.
        self.sdr.tx_hardwaregain_chan0 = self.tx_attenuation        # Attenuation applied to Tx path.

        self.sdr.rx_rf_bandwidth = int(self.sampling_frequency)     # Same as sampling rate.
        self.sdr.rx_lo = int(self.fsx)                              # Rx local oscillator.
        self.sdr.gain_control_mode_chan0 = "manual"                 # Turn off AGC.
        self.sdr.rx_hardwaregain_chan0 = 0                          # Rx gain.
        self.sdr.rx_buffer_size(self.rx_buffer_size)                # Rx buffer size.

    def pulse(self):
        self.sdr.tx_destroy_buffer()        # Must be used to send a different signal.
        self.sdr.tx(self.tx_signal)         # Send the pulse.
        time.sleep(self.dwell_time)         # Dwell time.
        self.rx_signal = self.sdr.rx()      # Pull Rx buffer.
