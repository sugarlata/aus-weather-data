from enum import Enum
from typing import List
from .utils import get_translation_coordinate


class RADAR_TYPE(Enum):
    '''
    Enum class for radar types across all locations
    '''

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


class BOMRadarLocationBase:
    '''
    Base Class for Radar Locations

    This forms the base class for all radar location classes.

    This class should not be directly called. Instead use a 
    nested class of :class:`aus_weather_data.radar.location.BOMRadarLocation`. 
    See BOMRadarLocation documentation for more details.
    '''

    _name: str = None
    _latitude: float = None
    _longitude: float = None
    _radar_types: List[RADAR_TYPE] = [
        RADAR_TYPE.REF_512_KM,
        RADAR_TYPE.REF_256_KM,
        RADAR_TYPE.REF_128_KM,
        RADAR_TYPE.RAI_128_KM_5M,
        RADAR_TYPE.RAI_128_KM_1H,
        RADAR_TYPE.RAI_128_KM_24H,
        RADAR_TYPE.RAI_128_KM_9AM,
    ]

    @classmethod
    def location(cls) -> tuple:
        '''Get the location (latitude and longitude) of the radar.

        Returns:
            Location of the radar
        '''

        return (cls._latitude, cls._longitude)

    @classmethod
    def name(cls) -> str:
        '''
        Get the name of the radar.

        Returns:
            Name of the radar
        '''

    @classmethod
    def radar_range(cls, radar_type: RADAR_TYPE) -> tuple:
        '''
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
        '''

        if radar_type not in RADAR_TYPE:
            raise TypeError("radar_type should be a RADAR_TYPE")

        if "64_KM" in radar_type.name:
            distance = 64
        elif "128_KM" in radar_type.name:
            distance = 128
        elif "256_KM" in radar_type.name:
            distance = 256
        elif "512_KM" in radar_type.name:
            distance = 512

        north_lat, _ = get_translation_coordinate(
            cls._latitude,
            cls._longitude,
            distance,
            0
        )
        south_lat, _ = get_translation_coordinate(
            cls._latitude,
            cls._longitude,
            distance,
            180
        )
        _, west_lon = get_translation_coordinate(
            cls._latitude,
            cls._longitude,
            distance,
            270
        )
        _, east_lon = get_translation_coordinate(
            cls._latitude,
            cls._longitude,
            distance,
            90
        )

        return (
            (north_lat, west_lon),
            (north_lat, east_lon),
            (south_lat, east_lon),
            (south_lat, west_lon)
        )


class BOMRadarLocation:
    '''
    Contains Radar Location Objects for Australia.

    These can be accessed using the format aus_weather_data.BOMRadarLocation.IDRXX

    For example::

        from aus_weather_data import BOMRadarLocation

        BOMRadarLocation.IDR02.get_location()

    Each class inherits from :class:`aus_weather_data.radar.location.BOMRadarLocationBase`

    .. todo:: The list of radar locations is incomplete. Requires completion for all stations. 

    '''

    class IDR02(BOMRadarLocationBase):
        '''
        IDR for Melbourne

        See :class:`aus_weather_data.radar.location.BOMRadarLocationBase` for inherited methods.
        '''

        _name = "Melbourne"
        _latitude = -37.86
        _longitude = 144.76

    class IDR49(BOMRadarLocationBase):
        '''
        IDR for Yarrawonga

        See :class:`aus_weather_data.radar.location.BOMRadarLocationBase` for inherited methods.
        '''

        _name = "Yarrawonga"
        _latitude = -36.03
        _longitude = 146.03

    class IDR68(BOMRadarLocationBase):
        '''
        IDR for Bairnsdale

        See :class:`aus_weather_data.radar.location.BOMRadarLocationBase` for inherited methods.
        '''

        _name = "Bairnsdale"
        _latitude = -37.89
        _longitude = 147.56

    class IDR95(BOMRadarLocationBase):
        '''
        IDR for Rainbow

        See :class:`aus_weather_data.radar.location.BOMRadarLocationBase` for inherited methods.
        '''

        _name = "Rainbow"
        _latitude = -35.99
        _longitude = 142.01

    class IDR97(BOMRadarLocationBase):
        '''
        IDR for Mildura

        See :class:`aus_weather_data.radar.location.BOMRadarLocationBase` for inherited methods.
        '''

        _name = "Mildura"
        _latitude = -34.28
        _longitude = 141.59

    class IDR55(BOMRadarLocationBase):
        '''
        IDR for Wagga Wagga

        See :class:`aus_weather_data.radar.location.BOMRadarLocationBase` for inherited methods.
        '''

        _name = "Wagga Wagga"
        _latitude = -35.17
        _longitude = 147.47

    class IDR71(BOMRadarLocationBase):
        '''
        IDR for Sydney

        See :class:`aus_weather_data.radar.location.BOMRadarLocationBase` for inherited methods.
        '''

        _name = "Sydney"
        _latitude = -33.701
        _longitude = 151.21

    class IDR03(BOMRadarLocationBase):
        '''
        IDR for Wollongong

        See :class:`aus_weather_data.radar.location.BOMRadarLocationBase` for inherited methods.
        '''

        _name = "Wollongong"
        _latitude = -34.264
        _longitude = 150.874

    class IDR96(BOMRadarLocationBase):
        '''
        IDR for Yeoval

        See :class:`aus_weather_data.radar.location.BOMRadarLocationBase` for inherited methods.
        '''

        _name = "Yeoval"
        _latitude = -32.74
        _longitude = 148.7

    class IDR40(BOMRadarLocationBase):
        '''
        IDR for Canberra

        See :class:`aus_weather_data.radar.location.BOMRadarLocationBase` for inherited methods.
        '''

        _name = "Canberra"
        _latitude = -35.66
        _longitude = 149.51

    class IDR94(BOMRadarLocationBase):
        '''
        IDR for Hillston

        See :class:`aus_weather_data.radar.location.BOMRadarLocationBase` for inherited methods.
        '''

        _name = "Hillston"
        _latitude = -33.55
        _longitude = 145.52

    class IDR64(BOMRadarLocationBase):
        '''
        IDR for Adelaide (Buckland Park)

        See :class:`aus_weather_data.radar.location.BOMRadarLocationBase` for inherited methods.
        '''

        _name = "Adelaide (Buckland Park)"
        _latitude = -34.617
        _longitude = 138.469

    class IDR46(BOMRadarLocationBase):
        '''
        IDR for Adelaide (Sellincks Hill)

        See :class:`aus_weather_data.radar.location.BOMRadarLocationBase` for inherited methods.
        '''

        _name = "Adelaide (Sellincks Hill)"
        _latitude = -35.33
        _longitude = 138.5

    class IDR33(BOMRadarLocationBase):
        '''
        IDR for Ceduna

        See :class:`aus_weather_data.radar.location.BOMRadarLocationBase` for inherited methods.
        '''

        _name = "Ceduna"
        _latitude = -32.13
        _longitude = 133.7
