import numpy as np
import scipy.constants as con
import time
import adi
import matplotlib.pyplot as plt

# Time delay
i = 0
td = 0
while i < 1000:
    t0, t1 = time.thread_time_ns(), time.thread_time_ns()
    td = max(td, t1 - t0)
    i += 1

# Setup(input):
resolution = 50                     # Range resolution in m.
maxRange = 5e3                      # Maximum range in m.
fc = int(5.8e9)                     # Carrier frequency.
fsx = 4                             # Fs = fsx*2*pulseBW. *has to be supported by the ADC
plutoIP = "192.168.2.1"

# Setup(calculations):
rangeSteps = int(maxRange/resolution)   # Number of range steps.
propSpeed = con.speed_of_light          # Propagation speed.
pulseBW = propSpeed/(2*resolution)      # Pulse bandwidth.
pulseWidth = 1/pulseBW                  # Pulse width in s.
fs = fsx*pulseBW                        # Sampling frequency.
prf = propSpeed/(2*maxRange)            # Repetition frequency.
numSamples = int((1/prf)*fs+2*fsx)      # Number of samples to process.

# Tx calculation:
txS = np.zeros(20)
txS[fsx:2*fsx] = 2**14             # samples are between -2^14 and +2^14

# SDR setup:
sdr = adi.Pluto(plutoIP)            # Connect to SDR.

# Tx setup:
#sdr.sample_rate = int(fs)                  # Send sampling rate (shared between Rx and Tx).
#sdr.tx_rf_bandwidth = int(fs/(2*fsx))      # Same as sampling rate.
#sdr.tx_lo = int(fc)                        # Tx local oscillator.
#sdr.tx_hardwaregain_chan0 = 0              # Attenuation applied to Tx path.

# Rx Setup:
#sdr.rx_rf_bandwidth = int(fs/(2*fsx))      # Same as sampling rate.
#sdr.rx_lo = int(fc)                        # Rx local oscillator.
#sdr.gain_control_mode_chan0 = "manual"     # Turn off AGC.
#sdr.rx_hardwaregain_chan0 = 0              # Rx gain.
#sdr.rx_buffer_size()                       # Rx buffer size.

#new comment

# Tx send:
#sdr.tx(txS)                        # Send the signal.
#sdr.tx_cyclic_buffer = True        # Enable cyclic buffers.
#sdr.tx_destroy_buffer()            # Must be used to send a different signal.
sdr.rx()

# output
print("Number of range steps:", rangeSteps)
print("Buffer size:", numSamples, 'samples.')
print("Pulse BW:", pulseBW/1000000, "MHz")
print("Sampling frequency:", fs/1000000, "MHz")
print("Pulse width:", pulseWidth*1e9, "ns")
print("Time delay:", td, "ns")
print("Steps skipped:", int(round(td/(pulseWidth*1e9))))
