import numpy as np
from numpy.typing import NDArray


def generate_road_profile(num_points: int = 100, x_max: float = 80) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """
    Generate a road profile using a clothoid-like approximation.

    A clothoid (Euler spiral) is a curve whose curvature increases linearly
    with its arc length. We'll approximate this with a polynomial curve.

    Parameters:
    -----------
    num_points : int
        Number of points to generate
    x_max : float
        Maximum x-coordinate value

    Returns:
    --------
    tuple of (np.array, np.array)
        x and y coordinates of the road profile
    """
    # Generate equidistant x points from 0 to x_max
    x = np.linspace(0, x_max, num_points)

    # Create a clothoid-like curve using a combination of polynomial
    # and sinusoidal terms
    # This creates a road that starts flat and gradually curves
    # Normalize x for the calculation
    x_norm = x / x_max

    # Clothoid approximation: starts flat, gradually increases curvature
    # Scale to keep maximum height around 8m (realistic road profile)
    y = (
        0.015 * x_norm**3 * x_max + 0.3 * np.sin(2 * np.pi * x_norm) + 0.035 * x_norm * x_max
    )  # PEP8 Violation: Missing space around =

    # Ensure it starts at (0, 0)
    y = y - y[0]

    return x, y  # PEP8 Violation: Missing space after comma
