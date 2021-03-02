# This is an example of using mySDRlib.
from mySDRlib import SDR
from DSP_tools import digital_signal
import numpy as np
import copy
import time
import matplotlib
import matplotlib.pyplot as plt
import scipy
from scipy import signal


matplotlib.use('TkAgg')

# These are the inputs to pass to the SDR:

resolution = 20                     # Range resolution in m.
max_range = 10e3                    # Maximum range in m.
fc = 5800e6                         # Carrier frequency.
fsx = 2                             # Fs = fsx*2*pulseBW. *has to be supported by the ADC
plutoIP = "ip:192.168.2.1"
tx_attenuation = 0                  # Attenuation applied to Tx path (0dB to -90dB).
num_pulses = 1                      # Number of pulses per trigger.
# create sdr object:
radar = SDR()


# set the parameters in program memory:
radar.resolution = resolution
radar.max_range = max_range
radar.carrier_frequency = fc
radar.fsx = fsx
radar.ip = plutoIP
radar.tx_attenuation = tx_attenuation
radar.num_pulses = num_pulses

# calculate the SDR parameters:
radar.calculate()

# connect to SDR:
radar.connect()

# send setup(after calculation):
radar.send_setup()
time.sleep(1)

# send and receive
radar.pulse()

print("Max range:", radar.max_range, "m")
print("Resolution:", radar.resolution, "m")
print("Number of range steps:", radar.range_steps, "steps")
print("Samples per step", radar.sample_per_step)
print("Pulse BW:", radar.pulse_BW/1e6, "MHz")
print("Pulse width:", radar.pulse_width*1e9, "ns")
print("Sampling frequency:", radar.sampling_frequency/1000000, "MHz")
print("Rx buffer size:", radar.rx_buffer_size, "samples")
print("Buffer time:", radar.dwell_time*1e6, "us")


s0 = digital_signal()
s0.fs = radar.sampling_frequency
s0.N = np.size(s0.x)
s0.x = np.abs(np.real(radar.rx_signal))
s0.mov_avg(radar.sample_per_step)
s0.gen_n()
s0.plot_signal(1)
plt.show()
