import math
import datetime


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


def split_filename(filename: str) -> dict:
    """Gets information from a filename

    Splits the information in a filename.

    Args:
        filename: Filename of the radar frame from BOM. E.G: IDR024.T.202001312236.png 

    Returns:
        Dictionary with the keys: [filename, idr, idrType, idrIdType, year, month, day, hour, minute, date, dt].
    """

    return {
        "filename": filename,
        "idr": filename[0:5],
        "idrType": filename[5:6],
        "idrIdType": filename[0:6],
        "year": filename[9:13],
        "month": filename[13:15],
        "day": filename[15:17],
        "hour": filename[17:19],
        "minute": filename[19:21],
        "date": '{year}-{month}-{day}'.format(
            year=filename[9:13],
            month=filename[13:15],
            day=filename[15:17]
        ),
        "dt": datetime.datetime.strptime(filename[9:21], "%Y%m%d%H%M").replace(tzinfo=datetime.timezone.utc)
    }
