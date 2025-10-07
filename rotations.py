import numpy as np

def givens_rotation(A, i, j, k, stable=True, impose_zero=False):
    """
    Apply a Givens rotation to zero out A[j, k] using A[i, k] as pivot.
    
    Parameters:
        A (ndarray): Input matrix.
        i (int): Pivot row index.
        j (int): Row index to be annihilated.
        k (int): Column index where elimination happens.
        stable (bool): If True, use np.hypot (numerically stable).
                       If False, use sqrt(a**2 + b**2) (naive).
    """
    A = np.array(A, dtype=float)  # copy
    
    a = A[i, k]
    b = A[j, k]

    if b == 0:
        return A  # nothing to do
    
    if stable:
        r = np.hypot(a, b)   # stable version
    else:
        r = np.sqrt(a**2 + b**2)  # naive version
    
    c = a / r
    s = b / r

    # Apply rotation
    row_i = A[i, :].copy()
    row_j = A[j, :].copy()

    A[i, :] = c * row_i + s * row_j
    A[j, :] = -s * row_i + c * row_j
    
    if impose_zero:
        A[j, k] = 0
    
    return A


def householder_transform(A, col_index):
    """
    Perform a Householder reflection on matrix A,
    zeroing out entries below the diagonal in the given column index.

    Parameters
    ----------
    A : np.ndarray
        Input matrix (m x n).
    col_index : int
        Column to transform (0-based).
        E.g. col_index=0 -> zero out A[1:,0],
             col_index=1 -> zero out A[2:,1], etc.

    Returns
    -------
    H : np.ndarray
        The Householder reflection matrix (m x m).
    R : np.ndarray
        The transformed matrix H @ A.
    """
    m, n = A.shape

    # Extract the vector we want to zero below the diagonal
    x = A[col_index:, col_index]  # subvector starting at (col_index, col_index)

    # Compute the norm of x
    norm_x = np.linalg.norm(x)

    # Choose sign to avoid cancellation
    sign = -1.0 if x[0] >= 0 else 1.0

    # Target vector (±||x||, 0, 0, …)
    e1 = np.zeros_like(x)
    e1[0] = 1.0
    v = x + sign * norm_x * e1  # reflection vector
    v = v / np.linalg.norm(v)   # normalize

    # Build the Householder reflector (only for the sub-block)
    H_sub = np.eye(m - col_index) - 2.0 * np.outer(v, v)

    # Expand to full H (block diagonal)
    H = np.eye(m)
    H[col_index:, col_index:] = H_sub

    # Apply transformation
    R = H @ A
    return H, R


def two_column_experiment_givens(left=31.0, right=47.0, height=7, second_column_rotation=False, impose_zero=False, stable=False):
    A = np.tile([left, right], (height, 1))
    A_rot = A

    # Option 2: full manual format
    print("\nFull precision manual format:")
    for row in A:
        print(" ".join(f"{val:.17e}" for val in row))

    for ele in range(height):
        current_ind = height - 1 - ele
        pivot = current_ind - 1
        if pivot < 0:
            break

        A_rot = givens_rotation(A_rot, i=pivot, j=current_ind, k=0, stable=stable, impose_zero=impose_zero)
        print(f"After left column H{ele+1}:\n", A_rot)  


    if second_column_rotation:
        for ele in range(height):
            current_ind = height - 1 - ele
            pivot = current_ind - 1
            if pivot < 1:
                break
                
            A_rot = givens_rotation(A_rot, i=pivot, j=current_ind, k=1, stable=stable, impose_zero=impose_zero)
            print(f"After right column  H{ele+1}:\n", A_rot)  



def two_column_experiment_householder(left=31.0, right=47.0, height=7):
    A = np.tile([left, right], (height, 1))
    A_rot = A

    # Option 2: full manual format
    print("\nFull precision manual format:")
    for row in A:
        print(" ".join(f"{val:.17e}" for val in row))

    # First Householder: zero below A[0,0]
    H1, R1 = householder_transform(A, col_index=0)
    
    # Second Householder: zero below A[1,1] in the transformed matrix
    H2, R2 = householder_transform(R1, col_index=1)
    
    print("After H1:\n", R1)
    print("After H2:\n", R2)  # This 
