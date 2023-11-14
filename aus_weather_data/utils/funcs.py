import math
import datetime


def calculate_translation(latitude, longitude, distance, bearing):

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
    return {"latitude": 180. * lat / math.pi, "longitude": 180. * lon / math.pi}


# def get_radar_metadata(idr):

#     radar_location = RADAR_LOCATIONS[idr]
#     name = radar_location["name"]
#     latitude = radar_location["latitude"]
#     longitude = radar_location["longitude"]

#     return {
#         "name": name,
#         "latitude": latitude,
#         "lonitude": longitude,
#         "1": {
#             "n": get_location(latitude, longitude, 512, 0),
#             "e": get_location(latitude, longitude, 512, 90),
#             "s": get_location(latitude, longitude, 512, 180),
#             "w": get_location(latitude, longitude, 512, 270),
#             "name": "Rain Rate 512km"
#         },
#         "2": {
#             "n": get_location(latitude, longitude, 256, 0),
#             "e": get_location(latitude, longitude, 256, 90),
#             "s": get_location(latitude, longitude, 256, 180),
#             "w": get_location(latitude, longitude, 256, 270),
#             "name": "Rain Rate 256km"
#         },
#         "3": {
#             "n": get_location(latitude, longitude, 128, 0),
#             "e": get_location(latitude, longitude, 128, 90),
#             "s": get_location(latitude, longitude, 128, 180),
#             "w": get_location(latitude, longitude, 128, 270),
#             "name": "Rain Rate 128km"
#         },
#         "4": {
#             "n": get_location(latitude, longitude, 64, 0),
#             "e": get_location(latitude, longitude, 64, 90),
#             "s": get_location(latitude, longitude, 64, 180),
#             "w": get_location(latitude, longitude, 64, 270),
#             "name": "Rain Rate 64km"
#         },
#         "I": {
#             "n": get_location(latitude, longitude, 128, 0),
#             "e": get_location(latitude, longitude, 128, 90),
#             "s": get_location(latitude, longitude, 128, 180),
#             "w": get_location(latitude, longitude, 128, 270),
#             "name": "Wind Velocity 128km"
#         },
#         "A": {
#             "n": get_location(latitude, longitude, 128, 0),
#             "e": get_location(latitude, longitude, 128, 90),
#             "s": get_location(latitude, longitude, 128, 180),
#             "w": get_location(latitude, longitude, 128, 270),
#             "name": "Rainfall Last 5 Minutes"
#         },
#         "B": {
#             "n": get_location(latitude, longitude, 128, 0),
#             "e": get_location(latitude, longitude, 128, 90),
#             "s": get_location(latitude, longitude, 128, 180),
#             "w": get_location(latitude, longitude, 128, 270),
#             "name": "Rainfall Last 1 Hour"
#         },
#         "C": {
#             "n": get_location(latitude, longitude, 128, 0),
#             "e": get_location(latitude, longitude, 128, 90),
#             "s": get_location(latitude, longitude, 128, 180),
#             "w": get_location(latitude, longitude, 128, 270),
#             "name": "Rainfall Since 9am"
#         },
#         "D": {
#             "n": get_location(latitude, longitude, 128, 0),
#             "e": get_location(latitude, longitude, 128, 90),
#             "s": get_location(latitude, longitude, 128, 180),
#             "w": get_location(latitude, longitude, 128, 270),
#             "name": "Rainfall Last 24 hours"
#         }
#     }


def split_filename(filename):

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
