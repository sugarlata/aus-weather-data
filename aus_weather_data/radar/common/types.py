from enum import Enum


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


RADAR_TYPE_MAP: dict[str:RADAR_TYPE] = {x.value: x for x in RADAR_TYPE}
