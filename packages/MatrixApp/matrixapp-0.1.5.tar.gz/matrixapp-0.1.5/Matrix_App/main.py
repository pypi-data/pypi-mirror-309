import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def check_function_max_min(m, n, b=None):
    """
    Param
    m = Matrix you want to check in np.array form
    n = Function Name in String
    b = Vector for linear system, optional (default: None)
    """
    if b is None:
        b = np.zeros(m.shape[0])  # Create a zero vector if b is None

    eigenvalues = np.linalg.eigvals(m)

    p_count, n_count = 0, 0
    for eig in eigenvalues:
        if eig > 0:
            p_count += 1
        elif eig < 0:
            n_count += 1

    minimum, maximum = False, False

    if p_count == len(eigenvalues):
        print(f"Function {n} has a minimum.")
        minimum = True
    elif n_count == len(eigenvalues):
        print(f"Function {n} has a maximum.")
        maximum = True
    else:
        print(f"Function {n} does not have a clear maximum or minimum.")
        return None  # Return None to indicate no clear max/min

    if minimum:
        print(f"Function {n} has a minimum at x = [0, 0, 0]. Minimum value: 0")
    elif maximum:
        print(f"Function {n} has a maximum at x = [0, 0, 0]. Maximum value: 0")

    try:
        x = np.dot(-np.linalg.inv(m), b)
        print(f"Solution to linear system: {x}")
    except np.linalg.LinAlgError:
        print("Matrix is singular, cannot compute inverse.")
        x = None

    if np.all(eigenvalues > 0):
        print(f"Function {n} has a global minimum.")
    elif np.all(eigenvalues < 0):
        print(f"Function {n} has a global maximum.")
    else:
        print(f"Function {n} does not have a global maximum or minimum.")

    return x  # Return x to capture the solution or None

import numpy as np

def compute_eigenvals_eigenvec(D):
    """
    Computes the covariance matrix, its eigenvalues, and eigenvectors for a given dataset D.
    
    Arguments:
        D: Array-like, shape (n, 2). The dataset to analyze.
    
    Returns:
        eigenvalues: Array of eigenvalues.
        eigenvectors: 2D array where each column is an eigenvector.
    """
    # Demean the dataset
    Demeaned = D - np.mean(D, axis=0)
    
    # Compute covariance matrix
    cov = np.dot(Demeaned.T, Demeaned) / len(D)
    
    # Compute eigenvalues and eigenvectors
    eigenvalues, eigenvectors = np.linalg.eig(cov)
    
    return Demeaned, cov, eigenvalues, eigenvectors


