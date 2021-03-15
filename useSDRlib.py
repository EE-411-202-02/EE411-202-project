# This is an example of using mySDRlib.
from mySDRlib import SDR
from DSP_tools import digital_signal
from signal_processor import process

import numpy as np
import copy
import time
import matplotlib
import matplotlib.pyplot as plt
import scipy
from scipy import signal


matplotlib.use('TkAgg')

# These are the inputs to pass to the SDR:

resolution = 10                    # Range resolution in m.
max_range = 2e3                     # Maximum range in m.
fc = 5800e6                         # Carrier frequency.
fsx = 1                             # Fs = fsx*2*pulseBW. *has to be supported by the ADC
plutoIP = "ip:192.168.2.1"
tx_attenuation = 0                  # Attenuation applied to Tx path (0dB to -90dB).
num_pulses = 3                      # Number of pulses per trigger.
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

# get noise floor:
radar.get_noise(500000)
spn = process(radar.rx_signal)
spn.filter(radar.sample_per_step)
spn.get_threshold()
print('Noise threshold:', spn.threshold)

plt.figure(1)
plt.plot(spn.si.hb[0:-1], spn.si.h)

# send and receive
radar.start_tx()
radar.get_rx()
radar.stop_tx()

sp = process(radar.rx_signal)
sp.filter(radar.sample_per_step)
sp.sync(radar.samples_per_scan)
print(np.size(sp.si.x))

sp.si.gen_n()
sp.si.stem_signal(2)
sp.detect(spn.threshold)
print('Detection at:', sp.d*radar.resolution)


print("Max range:", radar.max_range, "m")
print("Resolution:", radar.resolution, "m")
print("Number of range steps:", radar.range_steps, "steps")
print("Samples per step", radar.sample_per_step)
print("Pulse BW:", radar.pulse_BW/1e6, "MHz")
print("Pulse width:", radar.pulse_width*1e9, "ns")
print("Sampling frequency:", radar.sampling_frequency/1000000, "MHz")
print("Rx buffer size:", radar.rx_buffer_size, "samples")
print("Buffer time:", radar.dwell_time*1e6, "us")




plt.show()
#print(sp.temp)



#s0.add_samples(radar.sample_per_step)



