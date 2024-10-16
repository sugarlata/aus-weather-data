from typing import Set, Tuple, List
from aus_weather_data.radar.common.utils import get_translation_coordinate
from aus_weather_data.radar.common.types import RADAR_TYPE
from aus_weather_data.radar.common.idr_data import IDR_DATA


class BOMRadarLocationModel(object):
    """
    Base Class for Radar Location Data

    This is a middleware class that captures the data for a radar location.

    """

    def __init__(
        self,
        doc: str,
        base: str,
        location_name: str,
        latitude: float,
        longitude: float,
        radar_types: List[str],
    ):
        """Initialise the Radar Location Model

        Args:
            doc (str): Documentation for the radar location.
            base (str): Base of the radar (IDR02 for example).
            location_name (str): Name of the radar.
            latitude (float): Latitude of the radar.
            longitude (float): Longitude of the radar.
            radar_types (list[str]): List of radar types for this radar.

        """
        self.__doc__ = doc
        self._base = base
        self._location_name = location_name
        self._latitude = latitude
        self._longitude = longitude
        self._radar_types = {RADAR_TYPE(radar_type) for radar_type in radar_types}

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f"BOMRadarLocation<{self.base}: {self.location_name}>"

    @property
    def location(self) -> Tuple[float, float]:
        """
        Get the location (latitude and longitude) of the radar.

        Returns:
            (tuple[float, float]): Latitude and Longitude of the radar.
        """

        return (self._latitude, self._longitude)

    @property
    def location_name(self) -> str:
        """
        Get the name of the radar.

        Returns:
            (str): Name of the radar.
        """

        return self._location_name

    @property
    def base(self) -> str:
        """
        Get the base of the radar.

        Returns:
            (str): Radar Base
        """
        return self._base

    @property
    def radar_types(self) -> Set[RADAR_TYPE]:
        """
        Get the radar types for this radar.

        Returns:
            Radar types for this radar.
        """

        return self._radar_types

    def radar_range(self, radar_type: RADAR_TYPE) -> Tuple[tuple, tuple, tuple, tuple]:
        """
        Get the radar bounding box for a specific radar type

        This function will return the bounding box of the radar,
        for the given radar type. The bounding box will consist
        of four coordinates in the following order:

        #. North West
        #. North East
        #. South East
        #. South West

        Each entry is a tuple of form (lat, lon)

        Args:
            radar_type (RADAR_TYPE): The radar type to get the range for.

        Returns:
            (tuple) Four bounding corners of the range. Each corner is a tuple -> (lat, lon)

        Raises:
            TypeError: If the radar type is not of type :class:`RADAR_TYPE`
        """

        if radar_type not in RADAR_TYPE:
            raise TypeError("radar_type should be a RADAR_TYPE")

        if radar_type not in self._radar_types:
            raise TypeError(f"There is no {radar_type} for {self._location_name}")

        if "64_KM" in radar_type.name:
            distance = 64
        elif "128_KM" in radar_type.name:
            distance = 128
        elif "256_KM" in radar_type.name:
            distance = 256
        elif "512_KM" in radar_type.name:
            distance = 512

        north_lat, _ = get_translation_coordinate(
            self._latitude, self._longitude, distance, 0
        )
        south_lat, _ = get_translation_coordinate(
            self._latitude, self._longitude, distance, 180
        )
        _, west_lon = get_translation_coordinate(
            self._latitude, self._longitude, distance, 270
        )
        _, east_lon = get_translation_coordinate(
            self._latitude, self._longitude, distance, 90
        )

        return (
            (north_lat, west_lon),
            (north_lat, east_lon),
            (south_lat, east_lon),
            (south_lat, west_lon),
        )


class BOMRadarLocation:
    """Bureau of Meteorology Radar Locations

    This class contains the radar locations for the Bureau of Meteorology
    radar stations. Each radar station has a specific set of radar types
    that can be accessed.

    Use `IDR_LIST` for a list of all radar locations.

    """

    IDR02: BOMRadarLocationModel = BOMRadarLocationModel(**IDR_DATA["IDR02"])
    IDR49: BOMRadarLocationModel = BOMRadarLocationModel(**IDR_DATA["IDR49"])
    IDR68: BOMRadarLocationModel = BOMRadarLocationModel(**IDR_DATA["IDR68"])
    IDR95: BOMRadarLocationModel = BOMRadarLocationModel(**IDR_DATA["IDR95"])
    IDR97: BOMRadarLocationModel = BOMRadarLocationModel(**IDR_DATA["IDR97"])
    IDR55: BOMRadarLocationModel = BOMRadarLocationModel(**IDR_DATA["IDR55"])
    IDR71: BOMRadarLocationModel = BOMRadarLocationModel(**IDR_DATA["IDR71"])
    IDR03: BOMRadarLocationModel = BOMRadarLocationModel(**IDR_DATA["IDR03"])
    IDR96: BOMRadarLocationModel = BOMRadarLocationModel(**IDR_DATA["IDR96"])
    IDR40: BOMRadarLocationModel = BOMRadarLocationModel(**IDR_DATA["IDR40"])
    IDR94: BOMRadarLocationModel = BOMRadarLocationModel(**IDR_DATA["IDR94"])
    IDR64: BOMRadarLocationModel = BOMRadarLocationModel(**IDR_DATA["IDR64"])
    IDR46: BOMRadarLocationModel = BOMRadarLocationModel(**IDR_DATA["IDR46"])
    IDR33: BOMRadarLocationModel = BOMRadarLocationModel(**IDR_DATA["IDR33"])
    IDR66: BOMRadarLocationModel = BOMRadarLocationModel(**IDR_DATA["IDR66"])
    IDR50: BOMRadarLocationModel = BOMRadarLocationModel(**IDR_DATA["IDR50"])
    IDR108: BOMRadarLocationModel = BOMRadarLocationModel(**IDR_DATA["IDR108"])
    IDR08: BOMRadarLocationModel = BOMRadarLocationModel(**IDR_DATA["IDR08"])

    IDR_LIST = list(IDR_DATA.keys())


__all__ = [
    "BOMRadarLocation",
    "BOMRadarLocationModel",
]
