import math


def get_translation_coordinate(
    latitude: float, longitude: float, distance: float, bearing: float
) -> tuple:
    """
    Gets a coordinate a defined distance and heading away from a location

    Args:
        latitude: Latitude of the original location (in ° decimal)
        longitude: Longitude of the original location (in ° decimal)
        distance: Distance from the location (in kms)
        bearing: Heading of the second coordinate from the first (0 - 360 in ° decimal)
    Returns:
        tuple of format: (latitude, longitude)
    Raises:
        ValueError: If the distance is not a positive number
        ValueError: If the bearing is not a number between 0 and 360
        ValueError: If the latitude is not a number between -90 and 90
        ValueError: If the longitude is not a number between -180 and 180

    """

    # Guards
    if distance <= 0:
        raise ValueError("Distance must be a positive number")
    if bearing < 0 or bearing > 360:
        raise ValueError("Bearing must be a number between 0 and 360")
    if latitude < -90 or latitude > 90:
        raise ValueError("Latitude must be a number between -90 and 90")
    if longitude < -180 or longitude > 180:
        raise ValueError("Longitude must be a number between -180 and 180")



    R = 6378.1  # Radius of the Earth
    brng = math.pi * bearing / 180.0  # Convert bearing to radian
    lat = math.pi * latitude / 180.0  # Current coords to radians
    lon = math.pi * longitude / 180.0

    # Do the math magic
    lat = math.asin(
        math.sin(lat) * math.cos(distance / R)
        + math.cos(lat) * math.sin(distance / R) * math.cos(brng)
    )
    lon += math.atan2(
        math.sin(brng) * math.sin(distance / R) * math.cos(lat),
        math.cos(distance / R) - math.sin(lat) * math.sin(lat),
    )

    # Coords back to degrees and return
    return (round(180.0 * lat / math.pi, 5), round(180.0 * lon / math.pi, 5))


__all__ = [
    "get_translation_coordinate",
]
