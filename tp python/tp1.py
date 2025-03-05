import numpy as np
import matplotlib.pyplot as plt

# Task 1 (and 2 combined)
A = 1
f0 = 1000
fs = 5000
Ts = 1/fs

# Define a time vector for continuous signal and for sampling
# Note: Here we use a short time interval (scaled by Ts) for demonstration.
t = np.linspace(-5*Ts, 10*Ts, 100000)    # Continuous time vector
x0 = A * np.sin(2 * np.pi * f0 * t)        # Continuous signal

n = np.arange(-5*Ts, 10*Ts + Ts, Ts)       # Discrete sampling instants
x0_sampled = A * np.sin(2 * np.pi * f0 * n)  # Sampled signal

plt.figure(figsize=(10, 8))

# Frequency-domain plot (first subplot)
plt.subplot(2, 1, 1)

N = len(x0_sampled)
# Frequency vector: fftfreq returns frequencies in order, then shift makes it centered
f = np.fft.fftshift(np.fft.fftfreq(N, Ts))
# Compute FFT of the sampled signal and shift it so that zero frequency is in the middle
X = np.fft.fftshift(np.fft.fft(x0_sampled))

plt.plot(f, np.abs(X)/N, 'g', linewidth=1.5)
plt.title(f'Spectre fréquentiel - f0 = {f0} Hz, fs = {fs} Hz')
plt.xlabel("Fréquence (Hz)")
plt.ylabel("Amplitude")
plt.xlim([-fs/2, fs/2])
plt.grid(True)

# Time-domain plot (second subplot)
plt.subplot(2, 1, 2)

plt.plot(t, x0, 'b', linewidth=1.5, label='Signal continu')
plt.stem(n, x0_sampled, linefmt='r', markerfmt='ro', basefmt=' ', label='Signal échantillonné')
plt.title(f'Signal temporel - f0 = {f0} Hz, fs = {fs} Hz')
plt.xlabel("Temps (s)")
plt.ylabel("Amplitude")
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()