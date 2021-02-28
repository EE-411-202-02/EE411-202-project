# This is an example of using mySDRlib.
from mySDRlib import SDR

# These are the inputs to pass to the SDR:
resolution = 25                     # Range resolution in m.
max_range = 2e3                     # Maximum range in m.
fc = int(5.8e9)                     # Carrier frequency.
fsx = 4                             # Fs = fsx*2*pulseBW. *has to be supported by the ADC
plutoIP = "192.168.2.1"
tx_attenuation = 0                  # Attenuation applied to Tx path (0dB to -90dB).
num_pulses = 1                      # Number of pulses per trigger.
# create sdr object:
sdr = SDR()


# set the parameters in program memory:
sdr.resolution = resolution
sdr.max_range = max_range
sdr.fc = fc
sdr.fsx = fsx
sdr.ip = plutoIP
sdr.tx_attenuation = tx_attenuation
sdr.num_pulses = num_pulses
# calculate the SDR parameters:
sdr.calculate()

# connect to SDR:
# sdr.connect()

# send setup(after calculation):
# sdr.send_setup()

# send and receive
# sdr.pulse()

print("Max range:", sdr.max_range, "m")
print("Resolution:", sdr.resolution, "m")
print("Number of range steps:", sdr.range_steps, "steps")
print("Samples per step", sdr.sample_per_step)
print("Pulse BW:", sdr.pulse_BW/1e6, "MHz")
print("Pulse width:", sdr.pulse_width*1e9, "ns")
print("Sampling frequency:", sdr.sampling_frequency/1000000, "MHz")
print("Rx buffer size:", sdr.rx_buffer_size, "samples")
print("Buffer time:", sdr.dwell_time*1e6, "us")
