from enum import Enum
from typing import List, Set
from .utils import get_translation_coordinate
from .types import RADAR_TYPE


class BOMRadarLocationBase:
    """
    Base Class for Radar Locations

    This forms the base class for all radar location classes.

    This class should not be directly called. Instead use a
    nested class of :class:`aus_weather_data.radar.location.BOMRadarLocation`.
    See BOMRadarLocation documentation for more details.

    Attributes:
        _base_radar_types: Contains a list of the base radar types for all locations
    """

    _name: str
    _latitude: float
    _longitude: float
    _base_radar_types: Set[RADAR_TYPE] = {
        RADAR_TYPE.REF_512_KM,
        RADAR_TYPE.REF_256_KM,
        RADAR_TYPE.REF_128_KM,
    }
    radar_types: Set[RADAR_TYPE]

    @classmethod
    def location(cls) -> tuple:
        """Get the location (latitude and longitude) of the radar.

        Returns:
            Location of the radar
        """

        return (cls._latitude, cls._longitude)

    @classmethod
    def name(cls) -> str:
        """
        Get the name of the radar.

        Returns:
            Name of the radar
        """

        return cls._name

    @classmethod
    def base(cls):
        """
        Get the base of the radar.

        Returns:
            Radar Base
        """
        return cls.__name__

    @classmethod
    def radar_range(cls, radar_type: RADAR_TYPE) -> tuple:
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
            radar_type: The radar type requested for this bounding box.

        Returns:
            Four bounding corners of the range. Each corner is a tuple -> (lat, lon)

        Raises:
            TypeError: If the radar type is not of type :class:`RADAR_TYPE`
        """

        if radar_type not in RADAR_TYPE:
            raise TypeError("radar_type should be a RADAR_TYPE")

        if radar_type not in cls.radar_types:
            raise TypeError(f"There is no {radar_type} for {cls._name}")

        if "64_KM" in radar_type.name:
            distance = 64
        elif "128_KM" in radar_type.name:
            distance = 128
        elif "256_KM" in radar_type.name:
            distance = 256
        elif "512_KM" in radar_type.name:
            distance = 512

        north_lat, _ = get_translation_coordinate(
            cls._latitude, cls._longitude, distance, 0
        )
        south_lat, _ = get_translation_coordinate(
            cls._latitude, cls._longitude, distance, 180
        )
        _, west_lon = get_translation_coordinate(
            cls._latitude, cls._longitude, distance, 270
        )
        _, east_lon = get_translation_coordinate(
            cls._latitude, cls._longitude, distance, 90
        )

        return (
            (north_lat, west_lon),
            (north_lat, east_lon),
            (south_lat, east_lon),
            (south_lat, west_lon),
        )


class BOMRadarLocation:
    """
    Contains Radar Location Objects for Australia.

    These can be accessed using the format aus_weather_data.BOMRadarLocation.IDRXX

    For example::

        from aus_weather_data import BOMRadarLocation

        BOMRadarLocation.IDR02.get_location()

    Each class inherits from :class:`aus_weather_data.radar.location.BOMRadarLocationBase`

    .. todo:: The list of radar locations is incomplete. Requires completion for all stations.

    """

    class IDR02(BOMRadarLocationBase):
        """
        IDR for Melbourne

        See :class:`aus_weather_data.radar.location.BOMRadarLocationBase` for inherited methods.

        Attributes:
            radar_types: Contains a list of the radar types that this location supports.
        """

        _name = "Melbourne"
        _latitude = -37.86
        _longitude = 144.76
        radar_types: Set[RADAR_TYPE] = {
            *BOMRadarLocationBase._base_radar_types,
            RADAR_TYPE.REF_64_KM,
            RADAR_TYPE.VEL_128_KM,
            RADAR_TYPE.RAI_128_KM_1H,
            RADAR_TYPE.RAI_128_KM_24H,
            RADAR_TYPE.RAI_128_KM_5M,
            RADAR_TYPE.RAI_128_KM_9AM,
        }

    class IDR49(BOMRadarLocationBase):
        """
        IDR for Yarrawonga

        See :class:`aus_weather_data.radar.location.BOMRadarLocationBase` for inherited methods.

        Attributes:
            radar_types: Contains a list of the radar types that this location supports.
        """

        _name = "Yarrawonga"
        _latitude = -36.03
        _longitude = 146.03
        radar_types: Set[RADAR_TYPE] = {
            *BOMRadarLocationBase._base_radar_types,
            RADAR_TYPE.REF_64_KM,
            RADAR_TYPE.VEL_128_KM,
        }

    class IDR68(BOMRadarLocationBase):
        """
        IDR for Bairnsdale

        See :class:`aus_weather_data.radar.location.BOMRadarLocationBase` for inherited methods.

        Attributes:
            radar_types: Contains a list of the radar types that this location supports.
        """

        _name = "Bairnsdale"
        _latitude = -37.89
        _longitude = 147.56
        radar_types: Set[RADAR_TYPE] = {
            *BOMRadarLocationBase._base_radar_types,
            RADAR_TYPE.VEL_128_KM,
        }

    class IDR95(BOMRadarLocationBase):
        """
        IDR for Rainbow

        See :class:`aus_weather_data.radar.location.BOMRadarLocationBase` for inherited methods.

        Attributes:
            radar_types: Contains a list of the radar types that this location supports.
        """

        _name = "Rainbow"
        _latitude = -35.99
        _longitude = 142.01
        radar_types: Set[RADAR_TYPE] = {
            *BOMRadarLocationBase._base_radar_types,
            RADAR_TYPE.REF_64_KM,
            RADAR_TYPE.VEL_128_KM,
            RADAR_TYPE.RAI_128_KM_1H,
            RADAR_TYPE.RAI_128_KM_24H,
            RADAR_TYPE.RAI_128_KM_5M,
            RADAR_TYPE.RAI_128_KM_9AM,
        }

    class IDR97(BOMRadarLocationBase):
        """
        IDR for Mildura

        See :class:`aus_weather_data.radar.location.BOMRadarLocationBase` for inherited methods.

        Attributes:
            radar_types: Contains a list of the radar types that this location supports.
        """

        _name = "Mildura"
        _latitude = -34.28
        _longitude = 141.59
        radar_types: Set[RADAR_TYPE] = {
            *BOMRadarLocationBase._base_radar_types,
            RADAR_TYPE.REF_64_KM,
            RADAR_TYPE.VEL_128_KM,
            RADAR_TYPE.RAI_128_KM_1H,
            RADAR_TYPE.RAI_128_KM_24H,
            RADAR_TYPE.RAI_128_KM_5M,
            RADAR_TYPE.RAI_128_KM_9AM,
        }

    class IDR55(BOMRadarLocationBase):
        """
        IDR for Wagga Wagga

        See :class:`aus_weather_data.radar.location.BOMRadarLocationBase` for inherited methods.

        Attributes:
            radar_types: Contains a list of the radar types that this location supports.
        """

        _name = "Wagga Wagga"
        _latitude = -35.17
        _longitude = 147.47
        radar_types: Set[RADAR_TYPE] = {*BOMRadarLocationBase._base_radar_types}

    class IDR71(BOMRadarLocationBase):
        """
        IDR for Sydney

        See :class:`aus_weather_data.radar.location.BOMRadarLocationBase` for inherited methods.

        Attributes:
            radar_types: Contains a list of the radar types that this location supports.
        """

        _name = "Sydney"
        _latitude = -33.701
        _longitude = 151.21
        radar_types: Set[RADAR_TYPE] = {
            *BOMRadarLocationBase._base_radar_types,
            RADAR_TYPE.REF_64_KM,
            RADAR_TYPE.VEL_128_KM,
            RADAR_TYPE.RAI_128_KM_1H,
            RADAR_TYPE.RAI_128_KM_24H,
            RADAR_TYPE.RAI_128_KM_5M,
            RADAR_TYPE.RAI_128_KM_9AM,
        }

    class IDR03(BOMRadarLocationBase):
        """
        IDR for Wollongong

        See :class:`aus_weather_data.radar.location.BOMRadarLocationBase` for inherited methods.

        Attributes:
            radar_types: Contains a list of the radar types that this location supports.
        """

        _name = "Wollongong"
        _latitude = -34.264
        _longitude = 150.874
        radar_types: Set[RADAR_TYPE] = {
            *BOMRadarLocationBase._base_radar_types,
            RADAR_TYPE.REF_64_KM,
            RADAR_TYPE.VEL_128_KM,
            RADAR_TYPE.RAI_128_KM_1H,
            RADAR_TYPE.RAI_128_KM_24H,
            RADAR_TYPE.RAI_128_KM_5M,
            RADAR_TYPE.RAI_128_KM_9AM,
        }

    class IDR96(BOMRadarLocationBase):
        """
        IDR for Yeoval

        See :class:`aus_weather_data.radar.location.BOMRadarLocationBase` for inherited methods.

        Attributes:
            radar_types: Contains a list of the radar types that this location supports.
        """

        _name = "Yeoval"
        _latitude = -32.74
        _longitude = 148.7
        radar_types: Set[RADAR_TYPE] = {
            *BOMRadarLocationBase._base_radar_types,
            RADAR_TYPE.REF_64_KM,
            RADAR_TYPE.VEL_128_KM,
            RADAR_TYPE.RAI_128_KM_1H,
            RADAR_TYPE.RAI_128_KM_24H,
            RADAR_TYPE.RAI_128_KM_5M,
            RADAR_TYPE.RAI_128_KM_9AM,
        }

    class IDR40(BOMRadarLocationBase):
        """
        IDR for Canberra

        See :class:`aus_weather_data.radar.location.BOMRadarLocationBase` for inherited methods.

        Attributes:
            radar_types: Contains a list of the radar types that this location supports.
        """

        _name = "Canberra"
        _latitude = -35.66
        _longitude = 149.51
        radar_types: Set[RADAR_TYPE] = {
            *BOMRadarLocationBase._base_radar_types,
            RADAR_TYPE.REF_64_KM,
            RADAR_TYPE.VEL_128_KM,
            RADAR_TYPE.RAI_128_KM_1H,
            RADAR_TYPE.RAI_128_KM_24H,
            RADAR_TYPE.RAI_128_KM_5M,
            RADAR_TYPE.RAI_128_KM_9AM,
        }

    class IDR94(BOMRadarLocationBase):
        """
        IDR for Hillston

        See :class:`aus_weather_data.radar.location.BOMRadarLocationBase` for inherited methods.

        Attributes:
            radar_types: Contains a list of the radar types that this location supports.
        """

        _name = "Hillston"
        _latitude = -33.55
        _longitude = 145.52
        radar_types: Set[RADAR_TYPE] = {
            *BOMRadarLocationBase._base_radar_types,
            RADAR_TYPE.REF_64_KM,
            RADAR_TYPE.VEL_128_KM,
            RADAR_TYPE.RAI_128_KM_1H,
            RADAR_TYPE.RAI_128_KM_24H,
            RADAR_TYPE.RAI_128_KM_5M,
            RADAR_TYPE.RAI_128_KM_9AM,
        }

    class IDR64(BOMRadarLocationBase):
        """
        IDR for Adelaide (Buckland Park)

        See :class:`aus_weather_data.radar.location.BOMRadarLocationBase` for inherited methods.

        Attributes:
            radar_types: Contains a list of the radar types that this location supports.
        """

        _name = "Adelaide (Buckland Park)"
        _latitude = -34.617
        _longitude = 138.469
        radar_types: Set[RADAR_TYPE] = {
            *BOMRadarLocationBase._base_radar_types,
            RADAR_TYPE.REF_64_KM,
            RADAR_TYPE.VEL_128_KM,
            RADAR_TYPE.RAI_128_KM_1H,
            RADAR_TYPE.RAI_128_KM_24H,
            RADAR_TYPE.RAI_128_KM_5M,
            RADAR_TYPE.RAI_128_KM_9AM,
        }

    class IDR46(BOMRadarLocationBase):
        """
        IDR for Adelaide (Sellicks Hill)

        See :class:`aus_weather_data.radar.location.BOMRadarLocationBase` for inherited methods.

        Attributes:
            radar_types: Contains a list of the radar types that this location supports.
        """

        _name = "Adelaide (Sellicks Hill)"
        _latitude = -35.33
        _longitude = 138.5
        radar_types: Set[RADAR_TYPE] = {
            *BOMRadarLocationBase._base_radar_types,
            RADAR_TYPE.RAI_128_KM_1H,
            RADAR_TYPE.RAI_128_KM_24H,
            RADAR_TYPE.RAI_128_KM_5M,
            RADAR_TYPE.RAI_128_KM_9AM,
        }

    class IDR33(BOMRadarLocationBase):
        """
        IDR for Ceduna

        See :class:`aus_weather_data.radar.location.BOMRadarLocationBase` for inherited methods.

        Attributes:
            radar_types: Contains a list of the radar types that this location supports.
        """

        _name = "Ceduna"
        _latitude = -32.13
        _longitude = 133.7
        radar_types: Set[RADAR_TYPE] = {
            *BOMRadarLocationBase._base_radar_types,
            RADAR_TYPE.REF_64_KM,
            RADAR_TYPE.VEL_128_KM,
            RADAR_TYPE.RAI_128_KM_1H,
            RADAR_TYPE.RAI_128_KM_24H,
            RADAR_TYPE.RAI_128_KM_5M,
            RADAR_TYPE.RAI_128_KM_9AM,
        }


RADAR_LOCATION_MAP: dict[str, BOMRadarLocationBase] = {
    x.base(): x
    for x in BOMRadarLocation.__dict__.values()
    if isinstance(x, BOMRadarLocationBase)
}
