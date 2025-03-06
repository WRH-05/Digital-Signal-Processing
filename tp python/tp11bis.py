'''import numpy as np

N1 = 3
N2 = 4
N = N1 * N2

x = np.random.rand(N) * 10
resizedMatrice = x.reshape(N1, N2)

def computeWeight(N1, N2, N):
    W = np.zeros((N1, N2), dtype=complex)
    for n1 in range(N1):
        for k2 in range(N2):
            W[n1, k2] = np.exp(-2j * np.pi * n1 * k2 / N)
    return W

def fft1d(matrix, W1, W2):
    N1, N2 = matrix.shape
    X1 = np.dot(W1, matrix)
    print("Intermediate X1:")
    print(X1)
    X2 = np.dot(X1, W2)
    print("Intermediate X2:")
    print(X2)
    X = X2.flatten()
    return X

W1 = weightsCompute(N1, N1, N)
W2 = weightsCompute(N2, N2, N)

X = fft1d(resizedMatrice, W1, W2)

print("Matrix:")
print(resizedMatrice)
print("W1:")
print(W1)
print("W2:")
print(W2)
print("FFT Resultat:")
print(X)

fftResult = np.fft.fft(x)
print("Numpy FFT Resultat:")
print(fftResult)

if np.allclose(X, fftResult):
    print("Les deux résultats sont identiques")
else:
    print("Les deux résultats sont différents")#################################
import numpy as np

def reshape_vector(x, N1, N2):
    return np.reshape(x, (N1, N2))

def weightsCompute(N1, N2, N):
    W = np.zeros((N1, N2), dtype=complex)
    for n1 in range(N1):
        for k2 in range(N2):
            W[n1, k2] = np.exp(-2j * np.pi * n1 * k2 / N)
    return W

def fft1d(x, N1, N2):
    N = N1 * N2
    X = reshape_vector(x, N1, N2)

    # FFT sur les lignes (dimension N2)
    for n1 in range(N1):
        X[n1, :] = np.fft.fft(X[n1, :])

    # Application des poids
    W = weightsCompute(N1, N2, N)
    X = X * W

    # FFT sur les colonnes (dimension N1)
    for k2 in range(N2):
        X[:, k2] = np.fft.fft(X[:, k2])

    return X.flatten()

# Signal aléatoire de taille N=12
N1, N2 = 3, 4
N = N1 * N2
signal = np.random.rand(N)

# FFT composite
X_composite = fft1d(signal, N1, N2)

# FFT standard pour comparaison
X_standard = np.fft.fft(signal)

import matplotlib.pyplot as plt

plt.figure(figsize=(10, 5))
plt.plot(np.abs(X_composite), 'r', marker='o', label='FFT Composite')
plt.plot(np.abs(X_standard), 'b', marker='x', label='FFT Standard')
plt.title("Comparaison des amplitudes FFT Composite vs FFT Standard")
plt.xlabel("Échantillons")
plt.ylabel("Amplitude")
plt.legend()
plt.grid(True)
plt.show()'''
import numpy as np 

def reshape_vector(x, N1, N2):
    return np.reshape(x, (N1, N2))

def weightsCompute(N1, N2, N):
    W = np.zeros((N1, N2), dtype=complex)
    for n1 in range(N1):
        for k2 in range(N2):
            W[n1, k2] = np.exp(-2j * np.pi * n1 * k2 / N)
    return W

def fft1d(x, N1, N2):
    N = N1 * N2
    X = reshape_vector(x, N1, N2)
    for n1 in range(N1):
        X[n1, :] = np.fft.fft(X[n1, :])
    W = weightsCompute(N1, N2, N)
    X = X * W
    for k2 in range(N2):
        X[:, k2] = np.fft.fft(X[:, k2])
    return X.flatten()

N1, N2 = 3, 4
N = N1 * N2
signal = np.random.rand(N)
X_composite = fft1d(signal, N1, N2)
X_standard = np.fft.fft(signal)

W1 = computeWeight(N1, N1, N)
W2 = computeWeight(N2, N2, N)

X = fft1d(resizedMatrice, W1, W2)

print("Matrix:")
print(resizedMatrice)
print("W1:")
print(W1)
print("W2:")
print(W2)
print("FFT Resultat:")
print(X)

fftResult = np.fft.fft(x)
print("Numpy FFT Resultat:")
print(fftResult)

if np.allclose(X, fftResult):
    print("Les deux résultats sont identiques")
else:
    print("Les deux résultats sont différents")