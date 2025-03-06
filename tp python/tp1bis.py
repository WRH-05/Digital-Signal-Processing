import numpy as np

def composite_fft(x, N1, N2):
    """
    Compute the FFT of an input vector x (of length N = N1 * N2)
    using a composite FFT algorithm and then reorder the result so that
    it matches the order of np.fft.fft(x).
    
    The algorithm:
      1. For each 0 <= n1 < N1, extract the subsequence:
             x[n1], x[n1+N1], x[n1+2*N1], ...  (length N2)
      2. Compute an N2-point FFT on each subsequence (row FFT).
      3. Multiply each element by the twiddle factor:
             exp(-2πi * n1 * k2 / (N1*N2))
         where k2 is the index from the row FFT.
      4. For each k2, compute an N1-point FFT over the n1 index (column FFT).
      5. Flatten the resulting matrix in Fortran (column-major) order.
      6. Reorder the flattened result so that if the composite output
         is naturally indexed as i = n1 + N1*n2, we reassign it to the index
         j = n2 + N2*n1, which matches np.fft.fft(x).
    """
    N = N1 * N2
    x = np.asarray(x)
    if x.size != N:
        raise ValueError("Length of input x must equal N1 * N2.")
    
    # Step 1: Extract sub-sequences. For each n1 (0 <= n1 < N1),
    # the row n1 contains: x[n1], x[n1+N1], x[n1+2*N1], ..., length N2.
    X = np.empty((N1, N2), dtype=complex)
    for n1 in range(N1):
        X[n1, :] = x[n1::N1]
    
    # Step 2: Compute the FFT along each row (each sub-sequence of length N2).
    Y = np.fft.fft(X, axis=1)
    
    # Step 3: Multiply by the twiddle factors.
    # Here n1 is the row index and k2 is the frequency index from the row FFT.
    n1_idx = np.arange(N1).reshape(N1, 1)  # shape (N1, 1)
    k2_idx = np.arange(N2).reshape(1, N2)    # shape (1, N2)
    twiddle = np.exp(-2j * np.pi * n1_idx * k2_idx / N)
    Y_twiddled = Y * twiddle
    
    # Step 4: Compute the FFT along the columns (over the n1 index) for each column.
    Z = np.fft.fft(Y_twiddled, axis=0)
    
    # Step 5: Flatten the (N1 x N2) matrix in Fortran order.
    # This ordering gives composite indices:
    # composite_index = n1 + N1 * n2.
    composite_result = np.reshape(Z, N, order='F')
    
    # Step 6: Reorder the output so that it matches np.fft.fft(x).
    # The direct FFT ordering uses the mapping: direct_index = n2 + N2 * n1.
    result_correct = np.empty_like(composite_result)
    for n1 in range(N1):
        for n2 in range(N2):
            comp_index = n1 + N1 * n2       # current index in composite_result
            direct_index = n2 + N2 * n1       # desired index in direct FFT order
            result_correct[direct_index] = composite_result[comp_index]
    
    return result_correct

if __name__ == '__main__':
    # Set the composite dimensions: choose N1 and N2 so that N = N1*N2.
    N1, N2 = 4, 8  # For example, N = 32
    N = N1 * N2

    # Create a random complex input vector of length N.
    x = np.random.random(N) + 1j * np.random.random(N)

    # Compute the composite FFT.
    comp_result = composite_fft(x, N1, N2)
    # Compute the direct FFT using NumPy.
    direct_result = np.fft.fft(x)

    # Print both results.
    np.set_printoptions(precision=8, suppress=True)
    print("Composite FFT result (reordered):")
    print(comp_result)
    print("\nDirect FFT result:")
    print(direct_result)
    print("\nDifference (norm):", np.linalg.norm(comp_result - direct_result))
    
    # Verify that the composite FFT matches the direct FFT.
    if np.allclose(comp_result, direct_result):
        print("\nThe composite FFT matches the direct FFT.")
    else:
        print("\nMismatch between composite FFT and direct FFT.")
