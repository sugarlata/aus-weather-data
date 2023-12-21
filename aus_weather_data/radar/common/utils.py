import math
import datetime


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
    """
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


def split_filename(filename: str) -> dict:
    """Gets information from a filename

    Splits the information in a filename.

    Args:
        filename: Filename of the radar frame from BOM. E.G: IDR024.T.202001312236.png

    Returns:
        Dictionary with the keys: [filename, idr, idrType, idrIdType, year, month, day, hour, minute, date, dt].
    """

    filename_array = filename.split(".")
    if len(filename_array) != 4:
        raise ValueError("Filename is not in the correct format.")

    idr = filename_array[0][:-1]
    idrType = filename_array[0][-1:]
    idrIdType = filename_array[0]
    year = filename_array[2][0:4]
    month = filename_array[2][4:6]
    day = filename_array[2][6:8]
    hour = filename_array[2][8:10]
    minute = filename_array[2][10:12]
    date = "{year}-{month}-{day}".format(year=year, month=month, day=day)
    dt = datetime.datetime.strptime(filename_array[2], "%Y%m%d%H%M").replace(
        tzinfo=datetime.timezone.utc
    )

    return {
        "filename": filename,
        "idr": idr,
        "idrType": idrType,
        "idrIdType": idrIdType,
        "year": year,
        "month": month,
        "day": day,
        "hour": hour,
        "minute": minute,
        "date": date,
        "dt": dt,
    }
