import numpy as np
import matplotlib.pyplot as plt

A=1
f0=120
f1=30
fmax=f1+f0
fs=2*fmax
Ts=1/fs

t=np.linspace(-5*Ts, 10*Ts, 100000)
x0= A*np.sin(2*np.pi*f0*t)
n=np.arange(-5*Ts, 10*Ts + Ts, Ts)
x0_sampled=A*np.sin(2*np.pi*f0*n)
x1=x0*np.exp(-1j*2*np.pi*f1*t)
x1_sampled=x0_sampled*np.exp(-1j*2*np.pi*f1*n)

plt.figure(figsize=(10, 8))
plt.subplot(2,1,1)

N = len(x1_sampled)

f = np.fft.fftshift(np.fft.fftfreq(N, Ts))

X = np.fft.fftshift(np.fft.fft(x1_sampled))

plt.plot(f,np.abs(X)/N, 'g',linewidth=1.5)
plt.title(f'spectre frequentiel - f0= {f0} Hz, fs={fs} Hz')
plt.xlabel("frequence (Hz)")
plt.ylabel("Amplitude")
plt.xlim([-fs/2,fs/2])
plt.grid(True)

plt.subplot(2,1,2)

plt.plot(t,x1,'b',linewidth=1.5, label='signal continu')
plt.stem(n, x1_sampled, linefmt='r', markerfmt='ro', basefmt=' ',label='signal echantille')
plt.title(f'signal temporel - f0={f0} Hz, fs={fs} Hz')
plt.xlabel("temps(s)")
plt.ylabel("Amplitude")
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()