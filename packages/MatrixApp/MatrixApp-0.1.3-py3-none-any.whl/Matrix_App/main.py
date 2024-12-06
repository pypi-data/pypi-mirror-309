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

def generalized_rotation(m, theta_rad, direction, scaling=None, matrix_size=2):
    """
    Apply rotation and scaling to a set of points in an N-dimensional space.
    Arguments:
        m: 2D array-like containing points. Shape (n, matrix_size-1) for (N-1)-dimensional points.
        theta_rad: Rotation angle in radians (applicable to 2D and 3D subspaces).
        direction: 'c' for clockwise, 'cc' for counterclockwise (only affects 2D rotation).
        scaling: Scaling matrix. Default is None, which uses identity or default scaling.
        matrix_size: Size of the transformation matrix (e.g., 2 for 2x2, 3 for 3x3, etc.).
    Returns:
        Transformed coordinates.
    """
    if matrix_size < 2:
        raise ValueError("Matrix size must be at least 2.")

    # Handle input points and homogeneous coordinates if needed
    if matrix_size > 2:
        m = np.hstack((m, np.ones((m.shape[0], 1))))  # Convert to homogeneous coordinates

    # Adjust theta for clockwise rotation
    if direction == 'c':
        theta_rad = -theta_rad

    # Create rotation matrix
    rotation_matrix = np.eye(matrix_size)
    if matrix_size >= 2:  # Define rotation in the first two dimensions
        rotation_matrix[:2, :2] = [
            [np.cos(theta_rad), -np.sin(theta_rad)],
            [np.sin(theta_rad),  np.cos(theta_rad)]
        ]

    # Create scaling matrix
    if scaling is None:
        scaling = np.eye(matrix_size)  # Default scaling: Identity matrix
        if matrix_size >= 2:
            scaling[:2, :2] = [
                [2, 0],
                [0, 0.5]
            ]

    # Combine rotation and scaling
    transformation_matrix = rotation_matrix @ scaling

    # Apply transformation
    transformed_points = m @ transformation_matrix.T

    # Return transformed points, removing the homogeneous component if present
    if matrix_size > 2:
        return transformed_points[:, :-1]  # Discard the last column
    else:
        return transformed_points
