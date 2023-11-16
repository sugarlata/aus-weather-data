import math


def get_translation_coordinate(latitude: float, longitude: float, distance: float, bearing: float) -> tuple:
    """
    Gets a coordinate a defined distance and heading away from a location

    Args:
        latitude: Latitude of the original location (in ° decimal)
        longitude: Longitude of the original location (in ° decimal)
        distance: Distance from the location (in kms)
        bearing: Heading of the second coordinate from the first (0 - 360 in ° decimal)
    Returns:
        tuple of format: (latitude, longitude)
    """
    R = 6378.1                          # Radius of the Earth
    brng = math.pi * bearing / 180.     # Convert bearing to radian
    lat = math.pi * latitude / 180.     # Current coords to radians
    lon = math.pi * longitude / 180.

    # Do the math magic
    lat = math.asin(math.sin(lat) * math.cos(distance / R) +
                    math.cos(lat) * math.sin(distance / R) * math.cos(brng))
    lon += math.atan2(math.sin(brng) * math.sin(distance / R) *
                      math.cos(lat), math.cos(distance/R)-math.sin(lat)*math.sin(lat))

    # Coords back to degrees and return
    return (180. * lat / math.pi, 180. * lon / math.pi)
