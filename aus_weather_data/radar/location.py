from enum import Enum

class BOMRadarLocation:
    '''Base Class for a Radar Location
    
    This forms the base for all radar location classes.
    
    Attributes
    ----------
    RADAR_TYPE : Enum
        Enumerated values for radar types
    _name : str
        Friendly name of the radar location
    _latitude : float
        Location (latitude) of the radar
    _longitude : float
        Location (longitude) of the radar
    '''

    class RADAR_TYPE(Enum):
        '''Enum class for all basic radar types across all locations
        '''

        REF_128_KM = "3"
        REF_256_KM = "2"
        REF_512_KM = "1"
    
    _name = None
    _latitude = None
    _longitude = None

    @property
    @classmethod
    def location(cls):
        '''tuple : Returns the location of the radar in format (lat, lon)

        '''
        return (cls._latitude, cls._longitude)
    
    @classmethod
    def radar_range(cls, radar_type):
        '''Return the radar bounding box for a radar type

        Will return a tuple of length four containing the following corners of the bounding box:
         - North West
         - North East
         - South East
         - South West
        Each entry is a tuple of form (lat, lon)

        Parameters
        ----------
        radar_type : RADAR_TYPE
            What is the radar type of the bounding box requested

        Returns
        -------
        tuple
            Length 4 tuple with bounding corners

        '''
        if radar_type == cls.RADAR_TYPE:
            pass


class IDR02(BOMRadarLocation):

    _name = "Melbourne"
    _latitude = -37.86
    _longitude = 144.76
    


RADAR_LOCATIONS = {
    "IDR02": {"latitude": -37.86, "longitude": 144.76, "name": "Melbourne"},
    "IDR49": {"latitude": -36.03, "longitude": 146.03, "name": "Yarrawonga"},
    "IDR68": {"latitude": -37.89, "longitude": 147.56, "name": "Bairnsdale"},
    "IDR95": {"latitude": -35.99, "longitude": 142.01, "name": "Rainbow"},
    "IDR97": {"latitude": -34.28, "longitude": 141.59, "name": "Mildura"},
    "IDR55": {"latitude": -35.17, "longitude": 147.47, "name": "Wagga Wagga"},
    "IDR71": {"latitude": -33.701, "longitude": 151.21, "name": "Sydney"},
    "IDR03": {"latitude": -34.264, "longitude": 150.874, "name": "Wollongong"},
    "IDR96": {"latitude": -32.74, "longitude": 148.7, "name": "Yeoval"},
    "IDR40": {"latitude": -35.66, "longitude": 149.51, "name": "Canberra"},
    "IDR94": {"latitude": -33.55, "longitude": 145.52, "name": "Hillston"},
    "IDR64": {"latitude": -34.617, "longitude": 138.469, "name": "Adelaide (Buckland Park)"},
    "IDR46": {"latitude": -35.33, "longitude": 138.5, "name": "Adelaide (Sellincks Hill)"},
    "IDR33": {"latitude": -32.13, "longitude": 133.7, "name": "Ceduna"}
}
