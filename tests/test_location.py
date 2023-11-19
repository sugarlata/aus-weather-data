import os
import sys
import pytz
import base64
import datetime

if True:
    sys.path.insert(0, os.path.abspath("."))
    from aus_weather_data import BOMRadarLocation, RADAR_TYPE


def test_melbourne_radar_location():
    assert BOMRadarLocation.IDR02.name() == "Melbourne"
    assert BOMRadarLocation.IDR02.location() == (-37.86, 144.76)
    assert BOMRadarLocation.IDR02.radar_range(RADAR_TYPE.REF_64_KM) == (
        (-37.285074882984375, 144.03181231627426),
        (-37.285074882984375, 145.4881876837257),
        (-38.4349251170156, 145.4881876837257),
        (-38.4349251170156, 144.03181231627426)
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
    assert BOMRadarLocation.IDR68.name() == "Bairnsdale"
    assert BOMRadarLocation.IDR68.location() == (-37.89, 147.56)
    assert BOMRadarLocation.IDR68.radar_range(RADAR_TYPE.REF_128_KM) == (
        (-36.74014976596879, 146.10312031938372),
        (-36.74014976596879, 149.0168796806163),
        (-39.03985023403123, 149.0168796806163),
        (-39.03985023403123, 146.10312031938372)
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
