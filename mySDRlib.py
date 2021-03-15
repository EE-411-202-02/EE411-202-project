# This library contains functions used to interact with the Adalm Pluto SDR.

import numpy as np
import scipy.constants as con
import adi


class SDR:
    def __init__(self):
        # Input:
        self.resolution = 0             # Range resolution in m.
        self.max_range = 0              # Maximum range in m.
        self.carrier_frequency = 0      # Carrier frequency in Hz.
        self.fsx = 0                    # Fs = fsx*2*pulseBW. *has to be supported by the ADC
        self.ip = "0.0.0.0"             # SDR IP
        self.tx_attenuation = 0         # Attenuation applied to Tx path (0dB to -90dB).
        self.rx_gain = 60               # Rx hardware gain (0dB to 60dB).
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
        self.samples_per_scan = None    # Samples per scan.

    def calculate(self):
        # This function calculates the SDR parameters and generates the Tx pulse shape.
        # Calculate parameters:
        self.range_steps = int(self.max_range / self.resolution)            # Number of range steps.
        prop_speed = con.speed_of_light                                     # Speed of light (m/s).
        self.pulse_BW = prop_speed / (2 * self.resolution)                  # Pulse BW (Hz).
        self.pulse_width = 1 / self.pulse_BW                                # Pulse width (s).
        self.sampling_frequency = self.fsx * 2 * self.pulse_BW              # Sampling frequency (Hz).
        self.repetition_frequency = prop_speed/(2*self.max_range)           # Maximum repetition frequency.
        self.dwell_time = 1/self.repetition_frequency                       # Time per scan (s).
        self.num_samples = int(self.dwell_time * self.sampling_frequency)   # Number of samples per scan.
        self.sample_per_step = int(self.num_samples / self.range_steps)     # Number of samples per step.
        self.rx_buffer_size = int((self.num_pulses*self.range_steps*2)*self.sample_per_step)  # Size of the Rx buffer.
        self.samples_per_scan = self.sample_per_step * self.range_steps     # Samples per scan.

        # Generate pulse:
        self.tx_pulse = np.zeros(self.num_samples*2)
        d = 1
        self.tx_pulse[d * self.sample_per_step:(d + 1) * self.sample_per_step] = 1
        self.tx_pulse = self.tx_pulse * (2 ** 14)

    def connect(self):
        # This function connects to the SDR using the given IP address.
        self.sdr = adi.Pluto(self.ip)

    def send_setup(self):
        # This function sends the calculated parameters to the SDR.
        self.sdr.sample_rate = int(self.sampling_frequency)         # Send sampling rate (shared between Rx and Tx).
        self.sdr.tx_rf_bandwidth = int(self.sampling_frequency)     # Same as sampling rate.
        self.sdr.tx_lo = int(self.carrier_frequency)                # Tx local oscillator.
        self.sdr.tx_hardwaregain_chan0 = self.tx_attenuation        # Attenuation applied to Tx path.
        self.sdr.rx_rf_bandwidth = int(self.sampling_frequency)     # Same as sampling rate.
        self.sdr.rx_lo = int(self.carrier_frequency)                # Rx local oscillator.
        self.sdr.gain_control_mode_chan0 = "manual"                 # Turn off AGC.
        self.sdr.rx_hardwaregain_chan0 = self.rx_gain               # Rx gain.
        self.sdr.rx_buffer_size = self.rx_buffer_size               # Rx buffer size.
        self.sdr.rx_enabled_channels = [0]
        self.sdr.tx_enabled_channels = [0]

    def start_tx(self):
        self.sdr.tx_destroy_buffer()        # Must be used to send a different signal.
        self.sdr.tx_cyclic_buffer = True    # Cyclic buffer: ON
        self.sdr.tx(self.tx_pulse)          # Send the pulse.

    def stop_tx(self):
        self.sdr.tx_destroy_buffer()        # Must be used to send a different signal.
        self.sdr.tx_cyclic_buffer = False   # Cyclic buffer: OFF

    def get_rx(self):
        self.sdr.rx_destroy_buffer()        # Clear buffer.
        self.rx_signal = self.sdr.rx()      # Pull Rx buffer.

    def get_noise(self, n):
        self.sdr.rx_destroy_buffer()        # Clear buffer.
        self.sdr.rx_buffer_size = n         # Number of noise samples.
        self.rx_signal = self.sdr.rx()      # Pull Rx buffer.
        self.sdr.rx_buffer_size = self.rx_buffer_size  # Reset original buffer size.
