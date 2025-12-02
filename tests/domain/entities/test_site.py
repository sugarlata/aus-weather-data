import json
from typing import Set
import pytest

from aus_weather_data.common.utils import get_translation_coordinate
from aus_weather_data.domain.entities.radar.site import RADAR_TYPE, RADAR_DISTANCE_MAP


@pytest.mark.parametrize(
    "site_id, description, location_name, latitude, longitude, radar_types",
    [
        (
            "IDR02",
            "Melbourne radar station",
            "Melbourne",
            -37.86,
            144.76,
            {RADAR_TYPE.REF_128_KM},
        ),
        (
            "IDR49",
            "Yarrawonga radar station",
            "Yarrawonga",
            -36.03,
            146.03,
            {RADAR_TYPE.REF_128_KM},
        ),
        (
            "IDR68",
            "Bairnsdale radar station",
            "Bairnsdale",
            -37.89,
            147.56,
            {RADAR_TYPE.REF_128_KM},
        ),
    ],
)
def test_site_success(
    site_id: str,
    description: str,
    location_name: str,
    latitude: float,
    longitude: float,
    radar_types: Set[RADAR_TYPE],
):
    from aus_weather_data.domain.entities.radar.site import RadarSite

    site = RadarSite(
        site_id, description, location_name, latitude, longitude, radar_types
    )

    assert site.id == site_id
    assert site.description == description
    assert site.location_name == location_name
    assert site.latitude == latitude
    assert site.longitude == longitude
    assert site.radar_types == radar_types
    assert site.gps_location == (latitude, longitude)

    north_west, north_east, south_east, south_west = site.radar_range(
        RADAR_TYPE.REF_128_KM
    )

    # Calculate expected corners using the same logic as radar_range
    distance = RADAR_DISTANCE_MAP[RADAR_TYPE.REF_128_KM]
    north_lat, _ = get_translation_coordinate(latitude, longitude, distance, 0)
    south_lat, _ = get_translation_coordinate(latitude, longitude, distance, 180)
    _, west_lon = get_translation_coordinate(latitude, longitude, distance, 270)
    _, east_lon = get_translation_coordinate(latitude, longitude, distance, 90)

    expected_north_west = (north_lat, west_lon)
    expected_north_east = (north_lat, east_lon)
    expected_south_east = (south_lat, east_lon)
    expected_south_west = (south_lat, west_lon)

    assert north_west == expected_north_west
    assert north_east == expected_north_east
    assert south_east == expected_south_east
    assert south_west == expected_south_west
