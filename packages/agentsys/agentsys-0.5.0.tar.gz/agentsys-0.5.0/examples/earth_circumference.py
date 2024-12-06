"""
This module provides a function to calculate the circumference of Earth.
"""

import math

def calculate_earth_circumference(radius: float = 6371.0) -> float:
    """
    Calculate the circumference of the Earth.

    The function uses the formula 2 * pi * radius, where the default radius 
    is 6371.0 kilometers (the average radius of Earth).

    Args:
        radius (float): The radius of the Earth in kilometers. Defaults to 6371.0.

    Returns:
        float: The circumference of the Earth in kilometers.

    Note:
        This is an approximation as Earth is not a perfect sphere but an oblate spheroid,
        meaning it is slightly flattened at the poles and bulging at the equator.
        The radius used here is an average value.
    """
    # Calculate the circumference using the formula: C = 2πr
    circumference = 2 * math.pi * radius
    return circumference

if __name__ == "__main__":
    # Calculate and display Earth's circumference
    circumference = calculate_earth_circumference()
    print(f"Earth's circumference: {circumference:.2f} kilometers")
    print(f"                       {circumference * 0.621371:.2f} miles")
