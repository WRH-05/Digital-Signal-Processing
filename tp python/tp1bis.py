import numpy as np

def reshape_vector(x, N1, N2):
    """
    Reshape le vecteur x (de taille N1*N2) en une matrice de taille (N1, N2)
    en utilisant l'ordre colonne pour être cohérent avec la factorisation.
    """
    # Ici, l'ordre 'F' (Fortran) permet d'obtenir x(n1,n2) = x[n1 + n2*N1]
    return np.reshape(x, (N1, N2), order='F')

def weightsCompute(N1, N2, N):
    """
    Calcule la matrice de poids de taille (N1, N2) avec :
       W[n1, k2] = exp(-2j*pi * n1 * k2 / N)
    pour n1 = 0,...,N1-1 et k2 = 0,...,N2-1.
    """
    n1 = np.arange(N1).reshape(N1, 1)
    k2 = np.arange(N2).reshape(1, N2)
    return np.exp(-2j * np.pi * n1 * k2 / N)

def fft1d(x, N1, N2):
    """
    Implémente l'algorithme de la FFT composite pour un vecteur x de taille N1*N2.
    
    L'algorithme s'effectue en quatre étapes :
      1. Reshape du vecteur x en une matrice X de taille (N1, N2)
      2. Calcul de la DFT de taille N1 (sur la première dimension)
      3. Multiplication par les facteurs de twiddle exp(-2j*pi*k1*n2/N)
      4. Calcul de la DFT de taille N2 (sur la deuxième dimension)
    
    La sortie est ensuite reconstituée en un vecteur de taille N en utilisant l'ordre colonne.
    """
    N = N1 * N2

    # Étape 1 : Reshape
    x_matrix = reshape_vector(x, N1, N2)
    
    # Étape 2 : DFT sur la première dimension (de taille N1)
    n1 = np.arange(N1).reshape(N1, 1)
    k1 = np.arange(N1).reshape(1, N1)
    WN1 = np.exp(-2j * np.pi * n1 * k1 / N1)
    # Pour chaque colonne, on calcule la DFT de taille N1 :
    Y = np.dot(WN1, x_matrix)
    
    # Étape 3 : Application des facteurs twiddle
    # Pour chaque élément Y[k1, n2], on multiplie par exp(-2j*pi*(k1*n2)/N)
    k1_vals = np.arange(N1).reshape(N1, 1)
    n2_vals = np.arange(N2).reshape(1, N2)
    twiddle = np.exp(-2j * np.pi * k1_vals * n2_vals / N)
    Z = Y * twiddle
    
    # Étape 4 : DFT sur la deuxième dimension (de taille N2)
    n2 = np.arange(N2).reshape(N2, 1)
    k2 = np.arange(N2).reshape(1, N2)
    WN2 = np.exp(-2j * np.pi * n2 * k2 / N2)
    # Pour chaque ligne (indice k1 fixe), on calcule la DFT sur n2 :
    X_matrix = np.dot(Z, WN2)
    
    # Reconstitution en un vecteur de taille N en utilisant l'ordre colonne pour respecter l'indexation
    X_result = np.reshape(X_matrix, (N,), order='F')
    
    return X_result

# ---------------------------
# Partie test de l'algorithme
# ---------------------------

# Paramètres
N1 = 3
N2 = 4
N = N1 * N2

# Génération du signal aléatoire X de taille N multiplié par 10.
# Ici, on génère un signal complexe (on peut aussi utiliser un signal réel si désiré)
np.random.seed(0)  # pour rendre l'exemple reproductible
X = 10 * (np.random.rand(N) + 1j * np.random.rand(N))

# Calcul de la FFT via l'algorithme composite personnalisé
X_custom = fft1d(X, N1, N2)

# Calcul de la FFT avec la fonction prédéfinie numpy.fft.fft
X_builtin = np.fft.fft(X)

# Affichage des résultats
print("Signal X (d'entrée) :")
print(X)
print("\nFFT personnalisée (X_custom) :")
print(X_custom)
print("\nFFT de numpy.fft (X_builtin) :")
print(X_builtin)

# Comparaison : calcul de l'erreur (norme de la différence)
error = np.linalg.norm(X_custom - X_builtin)
print("\nErreur (norme de la différence) :", error)
