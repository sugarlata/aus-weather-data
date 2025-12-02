from typing import List, Set, Tuple
from dataclasses import dataclass

from enum import Enum

from aus_weather_data.common.utils import get_translation_coordinate


class RADAR_TYPE(Enum):
    """
    Enum class for radar types across all locations
    """

    REF_64_KM = "4"
    """
    Radar Reflectivity for 64km range

    (Selected Locations Only)
    """

    REF_128_KM = "3"
    """
    Radar Reflectivity for 128km range
    """

    REF_256_KM = "2"
    """
    Radar Reflectivity for 256km range
    """

    REF_512_KM = "1"
    """
    Radar Reflectivity for 512km range
    """

    VEL_128_KM = "I"
    """
    Radar Velocity for 128km range

    (Selected Locations Only)
    """

    RAI_128_KM_5M = "A"
    """
    Rainfall in last 5 minutes for 128km range
    """

    RAI_128_KM_1H = "B"
    """
    Rainfall in last 1 hour for 128km range
    """

    RAI_128_KM_9AM = "C"
    """
    Rainfall since 9am for 128km range
    """

    RAI_128_KM_24H = "D"
    """
    Rainfall in last 24 hours for 128km range
    """

    def __str__(self):
        return f"RADAR_TYPE<{self.name}>"

    def __repr__(self):
        return self.__str__()


RADAR_DISTANCE_MAP = {
    RADAR_TYPE.REF_64_KM: 64,
    RADAR_TYPE.REF_128_KM: 128,
    RADAR_TYPE.REF_256_KM: 256,
    RADAR_TYPE.REF_512_KM: 512,
    RADAR_TYPE.VEL_128_KM: 128,
    RADAR_TYPE.RAI_128_KM_5M: 128,
    RADAR_TYPE.RAI_128_KM_1H: 128,
    RADAR_TYPE.RAI_128_KM_9AM: 128,
    RADAR_TYPE.RAI_128_KM_24H: 128,
}


@dataclass(frozen=True)
class RadarSite:
    """
    Base Class for Radar Location Data

    This is a dataclass that captures the data for a radar location.

    """

    id: str
    description: str
    location_name: str
    latitude: float
    longitude: float
    radar_types: Set[RADAR_TYPE]

    def __str__(self) -> str:
        return f"RadarSite<{self.id}: {self.location_name}>"

    def __repr__(self) -> str:
        return self.__str__()

    @property
    def gps_location(self) -> Tuple[float, float]:
        """
        Get the GPS location (latitude and longitude) of the radar.

        Returns:
            (tuple[float, float]): Latitude and Longitude of the radar.
        """

        return (self.latitude, self.longitude)

    def radar_range(self, radar_type: RADAR_TYPE) -> Tuple[
        tuple[float, float],
        tuple[float, float],
        tuple[float, float],
        tuple[float, float],
    ]:
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

        if not isinstance(radar_type, RADAR_TYPE):
            raise ValueError("radar_type should be a RADAR_TYPE")

        if radar_type not in self.radar_types:
            raise ValueError(f"There is no {radar_type} for {self.location_name}")

        try:
            distance = RADAR_DISTANCE_MAP[radar_type]
        except KeyError:
            raise ValueError(
                f"Radar Type distance not captured for {radar_type} and radar {self.location_name}"
            )

        north_lat, _ = get_translation_coordinate(
            self.latitude, self.longitude, distance, 0
        )
        south_lat, _ = get_translation_coordinate(
            self.latitude, self.longitude, distance, 180
        )
        _, west_lon = get_translation_coordinate(
            self.latitude, self.longitude, distance, 270
        )
        _, east_lon = get_translation_coordinate(
            self.latitude, self.longitude, distance, 90
        )

        return (
            (north_lat, west_lon),
            (north_lat, east_lon),
            (south_lat, east_lon),
            (south_lat, west_lon),
        )
