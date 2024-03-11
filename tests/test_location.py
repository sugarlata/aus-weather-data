import os
import sys
import base64
import datetime

from aus_weather_data import BOMRadarLocation, RADAR_TYPE


def test_melbourne_radar_location():

    assert BOMRadarLocation.IDR02.location_name == "Melbourne"
    assert BOMRadarLocation.IDR02.base == "IDR02"
    assert BOMRadarLocation.IDR02.location == (-37.86, 144.76)
    assert BOMRadarLocation.IDR02.radar_range(RADAR_TYPE.REF_64_KM) == (
        (-37.28507, 144.03181),
        (-37.28507, 145.48819),
        (-38.43493, 145.48819),
        (-38.43493, 144.03181),
    )
    assert RADAR_TYPE.REF_64_KM in BOMRadarLocation.IDR02.radar_types
    assert RADAR_TYPE.REF_128_KM in BOMRadarLocation.IDR02.radar_types
    assert RADAR_TYPE.REF_256_KM in BOMRadarLocation.IDR02.radar_types
    assert RADAR_TYPE.REF_512_KM in BOMRadarLocation.IDR02.radar_types
    assert RADAR_TYPE.RAI_128_KM_1H in BOMRadarLocation.IDR02.radar_types
    assert RADAR_TYPE.RAI_128_KM_24H in BOMRadarLocation.IDR02.radar_types
    assert RADAR_TYPE.RAI_128_KM_5M in BOMRadarLocation.IDR02.radar_types
    assert RADAR_TYPE.RAI_128_KM_9AM in BOMRadarLocation.IDR02.radar_types
    assert RADAR_TYPE.VEL_128_KM in BOMRadarLocation.IDR02.radar_types


def test_bairnsdale_radar_location():
    assert BOMRadarLocation.IDR68.location_name == "Bairnsdale"
    assert BOMRadarLocation.IDR68.base == "IDR68"
    assert BOMRadarLocation.IDR68.location == (-37.89, 147.56)
    assert BOMRadarLocation.IDR68.radar_range(RADAR_TYPE.REF_128_KM) == (
        (-36.74015, 146.10312),
        (-36.74015, 149.01688),
        (-39.03985, 149.01688),
        (-39.03985, 146.10312),
    )
    assert RADAR_TYPE.REF_64_KM not in BOMRadarLocation.IDR68.radar_types
    assert RADAR_TYPE.REF_128_KM in BOMRadarLocation.IDR68.radar_types
    assert RADAR_TYPE.REF_256_KM in BOMRadarLocation.IDR68.radar_types
    assert RADAR_TYPE.REF_512_KM in BOMRadarLocation.IDR68.radar_types
    assert RADAR_TYPE.RAI_128_KM_1H not in BOMRadarLocation.IDR68.radar_types
    assert RADAR_TYPE.RAI_128_KM_24H not in BOMRadarLocation.IDR68.radar_types
    assert RADAR_TYPE.RAI_128_KM_5M not in BOMRadarLocation.IDR68.radar_types
    assert RADAR_TYPE.RAI_128_KM_9AM not in BOMRadarLocation.IDR68.radar_types
    assert RADAR_TYPE.VEL_128_KM in BOMRadarLocation.IDR68.radar_types
