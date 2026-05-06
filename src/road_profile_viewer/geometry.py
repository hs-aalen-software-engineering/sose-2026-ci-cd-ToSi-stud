import numpy as np
from numpy.typing import NDArray


def calculate_ray_line(
    angle_degrees: float,
    camera_x: float = 0,
    camera_y: float = 2.0,
    x_max: float = 80,
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """
    Calculate the line representing the camera ray.

    Parameters:
    -----------
    angle_degrees : float
        Angle in degrees from the positive x-axis (measured downward from horizontal)
    camera_x : float
        X-coordinate of camera position
    camera_y : float
        Y-coordinate of camera position
    x_max : float
        Maximum x extent for the ray

    Returns:
    --------
    tuple of (np.array, np.array)
        x and y coordinates of the ray line
    """
    # Convert angle to radians (angle is measured downward from horizontal)
    # Negative angle because y-axis points up but we measure downward angle
    angle_rad = -np.deg2rad(angle_degrees)

    # Calculate slope
    if np.abs(np.cos(angle_rad)) < 1e-10:
        # Vertical line case
        return np.array([camera_x, camera_x]), np.array([camera_y, -10])

    slope = np.tan(angle_rad)

    # Calculate x range where the ray is valid
    # The ray should extend from the camera to where it would intersect y=0 or beyond
    if angle_degrees < 0 or angle_degrees > 180:
        # Ray going upward - just show a short segment
        x_end = min(camera_x + 20, x_max)
    else:
        # Ray going downward - extend to x_max
        x_end = x_max

    # Generate points for the ray
    x_ray = np.array([camera_x, x_end])
    y_ray = camera_y + slope * (x_ray - camera_x)

    return x_ray, y_ray


def find_intersection(
    x_road: NDArray[np.float64],
    y_road: NDArray[np.float64],
    angle_degrees: float,
    camera_x: float = 0,
    camera_y: float = 2.0,
) -> tuple[float | None, float | None, float | None]:
    """
    Find the intersection point between the camera ray and the road profile.

    Parameters:
    -----------
    x_road : np.array
        X-coordinates of the road profile
    y_road : np.array
        Y-coordinates of the road profile
    angle_degrees : float
        Angle of the camera ray in degrees
    camera_x : float
        X-coordinate of camera position
    camera_y : float
        Y-coordinate of camera position

    Returns:
    --------
    tuple of (float, float, float) or (None, None, None)
        x, y coordinates of intersection and distance from camera,
        or None if no intersection
    """
    angle_rad = -np.deg2rad(angle_degrees)

    # Handle vertical ray (angle ≈ 90°): ray travels straight down at x = camera_x
    if np.abs(np.cos(angle_rad)) < 1e-10:
        for i in range(len(x_road) - 1):
            x1, x2 = x_road[i], x_road[i + 1]
            if x1 <= camera_x <= x2:
                # x2 == x1 would mean two road points share the same x, which is
                # invalid for a function-like profile; fall back to segment start.
                t = (camera_x - x1) / (x2 - x1) if x2 != x1 else 0
                y_road_at_camera = y_road[i] + t * (y_road[i + 1] - y_road[i])
                # A downward ray only intersects the road when the camera is above it.
                # If the camera is at or below the road surface there is no intersection.
                if camera_y > y_road_at_camera:
                    distance = float(camera_y - y_road_at_camera)
                    return float(camera_x), float(y_road_at_camera), distance
        return None, None, None

    slope = np.tan(angle_rad)

    # Ray equation: y = camera_y + slope * (x - camera_x)
    # Check each segment of the road for intersection
    for i in range(len(x_road) - 1):
        x1, y1 = x_road[i], y_road[i]
        x2, y2 = x_road[i + 1], y_road[i + 1]

        # Skip if this segment is behind the camera
        if x2 <= camera_x:
            continue

        # Calculate y values of the ray at x1 and x2
        ray_y1 = camera_y + slope * (x1 - camera_x)
        ray_y2 = camera_y + slope * (x2 - camera_x)

        # Check if the ray crosses the road segment
        # The ray intersects if it's on different sides of the road at x1 and x2
        diff1 = ray_y1 - y1
        diff2 = ray_y2 - y2

        if diff1 * diff2 <= 0:  # Sign change or zero indicates intersection
            # Linear interpolation to find exact intersection point
            if abs(diff2 - diff1) < 1e-10:
                # Parallel lines
                t = 0
            else:
                t = diff1 / (diff1 - diff2)

            # Interpolate to find intersection point
            x_intersect = x1 + t * (x2 - x1)
            y_intersect = y1 + t * (y2 - y1)

            # Calculate distance from camera to intersection
            distance = np.sqrt((x_intersect - camera_x) ** 2 + (y_intersect - camera_y) ** 2)

            return x_intersect, y_intersect, distance

    return None, None, None
