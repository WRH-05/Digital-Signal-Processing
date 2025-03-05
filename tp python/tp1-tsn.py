import numpy as np
import matplotlib.pyplot as plt

# Ensure figure backgrounds are white
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = 'white'

def downsample_array(arr, max_points=2000):
    """Downsample a NumPy array to at most max_points elements."""
    if arr.size > max_points:
        factor = arr.size // max_points
        return arr[::factor]
    return arr

# ---------------------------
# Task 1: Plot x0(t) = A * sin(2πf0t)
# ---------------------------
def task1_plot_signal():
    A = 1
    # f0 values: 500 Hz, 1 kHz, 10 kHz
    f0_values = [500, 1000, 10000]
    # Sampling rates: 500 Hz, 1 kHz, 5 kHz, 50 kHz
    sampling_rates = [500, 1000, 5000, 50000]
    t_start, t_end = -5, 10  # seconds

    # Continuous (true) signal at high resolution
    t_cont = np.linspace(t_start, t_end, 10000)
    
    for f0 in f0_values:
        plt.figure(figsize=(10, 6))
        x_cont = A * np.sin(2 * np.pi * f0 * t_cont)
        plt.plot(t_cont, x_cont, 'k--', linewidth=2, label=f"True signal (f0={f0} Hz)")
        
        for fs in sampling_rates:
            dt = 1 / fs
            t_sample = np.arange(t_start, t_end, dt)
            x_sample = A * np.sin(2 * np.pi * f0 * t_sample)
            # Downsample the data for plotting
            t_sample_ds = downsample_array(t_sample)
            x_sample_ds = downsample_array(x_sample)
            plt.plot(t_sample_ds, x_sample_ds, 'o', markersize=3, label=f"fs={fs} Hz")
        
        plt.title(f"Task 1: x0(t) with f0 = {f0} Hz")
        plt.xlabel("Time (s)")
        plt.ylabel("Amplitude")
        plt.legend(fontsize=9)
        plt.grid(True)
        plt.tight_layout()
        plt.show()

# ---------------------------
# Task 2: FFT of x0(t) for f0 = 500 Hz, fs = 10 kHz
# ---------------------------
def task2_fft_signal():
    A = 1
    f0 = 500      # Hz
    fs = 10000    # Hz
    t_start, t_end = -5, 10

    t = np.arange(t_start, t_end, 1/fs)
    x = A * np.sin(2 * np.pi * f0 * t)
    
    # Compute FFT and frequency bins
    N = len(t)
    X = np.fft.fft(x)
    freqs = np.fft.fftfreq(N, d=1/fs)
    half_N = N // 2
    
    plt.figure(figsize=(10, 8))
    # Time domain plot
    plt.subplot(2, 1, 1)
    plt.plot(t, x, 'b-', linewidth=1.5)
    plt.title("Task 2: Time Domain Signal x0(t)")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.grid(True)
    
    # Frequency domain plot (only positive frequencies)
    plt.subplot(2, 1, 2)
    plt.plot(freqs[:half_N], np.abs(X[:half_N]) / N, 'r-', linewidth=1.5)
    plt.title("Task 2: Spectrum of x0(t)")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Normalized Amplitude")
    plt.grid(True)
    
    plt.tight_layout()
    plt.show()

# ---------------------------
# Task 3: Plot modulated signal x1(t) = x0(t)*exp(-j2πf1t) (magnitude)
#         with f0 in [120, 200] Hz and f1 in [30, 60] Hz.
# ---------------------------
def task3_modulated_signal():
    A = 1
    f0_values = [120, 200]  # Hz
    f1_values = [30, 60]    # Hz
    sampling_rates = [500, 1000, 5000, 50000]  # Hz
    t_start, t_end = -5, 10

    t_cont = np.linspace(t_start, t_end, 10000)
    
    for f0 in f0_values:
        for f1 in f1_values:
            plt.figure(figsize=(10, 6))
            # Continuous modulated signal (magnitude)
            x_cont = A * np.sin(2 * np.pi * f0 * t_cont) * np.exp(-1j * 2 * np.pi * f1 * t_cont)
            plt.plot(t_cont, np.abs(x_cont), 'k--', linewidth=2, label="True |x1(t)|")
            
            for fs in sampling_rates:
                dt = 1 / fs
                t_sample = np.arange(t_start, t_end, dt)
                x_sample = A * np.sin(2 * np.pi * f0 * t_sample) * np.exp(-1j * 2 * np.pi * f1 * t_sample)
                # Downsample for plotting if necessary
                t_sample_ds = downsample_array(t_sample)
                x_sample_ds = downsample_array(np.abs(x_sample))
                plt.plot(t_sample_ds, x_sample_ds, 'o', markersize=3, label=f"fs={fs} Hz")
            
            plt.title(f"Task 3: |x1(t)| with f0={f0} Hz, f1={f1} Hz")
            plt.xlabel("Time (s)")
            plt.ylabel("Magnitude")
            plt.legend(fontsize=9)
            plt.grid(True)
            plt.tight_layout()
            plt.show()

# ---------------------------
# Task 4: FFT of |x1(t)| for f0 = 200 Hz, f1 = 30 Hz, fs = 5000 Hz
# ---------------------------
def task4_fft_modulated_signal():
    A = 1
    f0 = 200  # Hz
    f1 = 30   # Hz
    fs = 5000 # Hz
    t_start, t_end = -5, 10

    t = np.arange(t_start, t_end, 1/fs)
    x = A * np.sin(2 * np.pi * f0 * t) * np.exp(-1j * 2 * np.pi * f1 * t)
    x_mag = np.abs(x)
    
    # Compute FFT and frequency bins
    N = len(x_mag)
    X = np.fft.fft(x_mag)
    freqs = np.fft.fftfreq(N, d=1/fs)
    half_N = N // 2
    
    plt.figure(figsize=(10, 8))
    # Time domain plot of |x1(t)|
    plt.subplot(2, 1, 1)
    plt.plot(t, x_mag, 'b-', linewidth=1.5)
    plt.title("Task 4: Time Domain |x1(t)|")
    plt.xlabel("Time (s)")
    plt.ylabel("Magnitude")
    plt.grid(True)
    
    # Frequency domain plot (FFT of |x1(t)|)
    plt.subplot(2, 1, 2)
    plt.plot(freqs[:half_N], np.abs(X[:half_N]) / N, 'r-', linewidth=1.5)
    plt.title("Task 4: Spectrum of |x1(t)|")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Normalized Amplitude")
    plt.grid(True)
    
    plt.tight_layout()
    plt.show()

# ---------------------------
# Main execution: run all tasks sequentially
# ---------------------------
if __name__ == "__main__":
    print("Running Task 1: Plot x0(t)")
    task1_plot_signal()
    
    print("Running Task 2: FFT of x0(t)")
    task2_fft_signal()
    
    print("Running Task 3: Plot modulated signal x1(t)")
    task3_modulated_signal()
    
    print("Running Task 4: FFT of |x1(t)|")
    task4_fft_modulated_signal()
