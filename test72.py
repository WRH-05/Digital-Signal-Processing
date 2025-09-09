import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# Parameters
slots_per_revolution = 72
motor_rpm = 1000
sampling_rate = 100000  # 100 kHz
duration = 0.01  # 10 milliseconds

# Calculations
motor_rps = motor_rpm / 60
pulse_frequency = slots_per_revolution * motor_rps

# Time array
t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)

# Generate square wave signal
square_wave = signal.square(2 * np.pi * pulse_frequency * t)

# Plotting
plt.figure(figsize=(10, 4))
plt.plot(t, square_wave, linewidth=2)
plt.title('Photodetector Output Signal')
plt.xlabel('Time (seconds)')
plt.ylabel('Amplitude')
plt.xlim(0, 5 / pulse_frequency)  # Displaying 5 periods
plt.grid(True)
plt.show()
