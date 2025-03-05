import numpy as np

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