import numpy as np
import matplotlib.pyplot as plt

A0 = 1
f0 = 100  # Hz
f1 = 200  # Hz
A1 = 2.5
Theta0 = 0  
fe = 2000  
T = 1  
t = np.linspace(0, 2*T)

x = A0 * np.cos(2 * np.pi * f0 * t) + A1 * np.sin(2 * np.pi * f1 * t + Theta0)

plt.figure(figsize=(12, 6))
plt.subplot(211)
plt.plot(t, x)
plt.title("Signal x(n)")
plt.xlabel("temp (s)")
plt.ylabel("Amplitude")
plt.grid()

#X = np.fft.fft(x)
#frequencies = np.fft.fftfreq(len(X), d=1/fe)


N = len(x)
f = np.fft.fftshift(np.fft.fftfreq(N, 1/fe))
X = np.fft.fftshift(np.fft.fft(x))




plt.subplot(212)
#plt.plot(frequencies[:len(frequencies)//2], np.abs(X[:len(X)//2]))
plt.plot(f, np.abs(X)/N, 'g', linewidth=1.5)
plt.title("FFT de x(n)")
plt.xlabel("Frequence (Hz)")
plt.ylabel("amplitude")
plt.grid()
plt.tight_layout()
plt.show()






















'''
# Butterworth filter design
def butter_bandpass(lowcut, highcut, fs, order=3):
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    return b, a

def apply_filter(data, lowcut, highcut, fs, order=3):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = filtfilt(b, a, data)
    return y

# Filter the signal for [50, 150] Hz
lowcut1, highcut1 = 50, 150
x_filtered1 = apply_filter(x, lowcut1, highcut1, fe)

# Filter the signal for [150, 250] Hz
lowcut2, highcut2 = 150, 250
x_filtered2 = apply_filter(x, lowcut2, highcut2, fe)

# Plot the filtered signals
plt.figure(figsize=(12, 6))
plt.subplot(2, 1, 1)
plt.plot(t, x_filtered1)
plt.title("Filtered Signal (50-150 Hz)")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.grid()

plt.subplot(2, 1, 2)
plt.plot(t, x_filtered2)
plt.title("Filtered Signal (150-250 Hz)")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.grid()
plt.tight_layout()
plt.show()'''