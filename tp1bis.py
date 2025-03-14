import numpy as np
import matplotlib.pyplot as plt

def fftComposite(x, N1, N2):
    N = N1 * N2
    x = np.asarray(x)
    if x.size != N:
        raise ValueError("La taille de x doit être égale à N1 * N2.")
    X = np.empty((N1, N2), dtype=complex)
    for n1 in range(N1):
        X[n1, :] = x[n1::N1]
    Y = np.fft.fft(X, axis=1)
    n1_idx = np.arange(N1).reshape(N1, 1)
    k2_idx = np.arange(N2).reshape(1, N2)
    poids = np.exp(-2j * np.pi * n1_idx * k2_idx / N)
    Y_rot = Y * poids
    Z = np.fft.fft(Y_rot, axis=0)
    res_composite = np.reshape(Z, N, order='F')
    res_final = np.empty_like(res_composite)
    for n1 in range(N1):
        for n2 in range(N2):
            idx_composite = n1 + N1 * n2
            idx_direct = n2 + N2 * n1
            res_final[idx_direct] = res_composite[idx_composite]
    return res_final

if __name__ == '__main__':

    N1, N2 = 4, 8
    N = N1 * N2
    x = np.random.random(N) + 1j * np.random.random(N)
    
    resultat_composite = fftComposite(x, N1, N2)
    resultat_direct = np.fft.fft(x)
    np.set_printoptions(precision=8, suppress=True)
    print("Résultat FFT composite (réordonné) :")
    print(resultat_composite)
    print("\nRésultat FFT direct :")
    print(resultat_direct)
    print("\nDifférence (norme) :", np.linalg.norm(resultat_composite - resultat_direct))

    if np.allclose(resultat_composite, resultat_direct):
        print("\nLes deux résultats sont identiques.")
    else:
        print("\nLes deux résultats sont différents.")

    
    plt.figure(figsize=(10, 5))
    plt.plot(np.abs(resultat_composite), 'r', marker='o', label='FFT Composite')
    plt.plot(np.abs(resultat_direct), 'b', marker='x', label='FFT Standard')
    plt.title("Comparaison des amplitudes FFT Composite vs FFT Standard")
    plt.xlabel("Échantillons")
    plt.ylabel("Amplitude")
    plt.legend()
    plt.grid(True)
    plt.show()
