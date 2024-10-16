from aus_weather_data.radar.common.types import RADAR_TYPE
from aus_weather_data.radar.common.location import (
    BOMRadarLocation,
    BOMRadarLocationModel,
)


def test_radar_locations():

    from aus_weather_data.radar.common.idr_data import IDR_DATA

    for base in IDR_DATA.keys():

        radar_location: BOMRadarLocationModel = getattr(BOMRadarLocation, base)  # type: ignore

        assert radar_location.location_name == IDR_DATA[base]["location_name"]
        assert radar_location.base == IDR_DATA[base]["base"]
        assert radar_location.location == (
            IDR_DATA[base]["latitude"],
            IDR_DATA[base]["longitude"],
        )
        assert radar_location.radar_types == {
            RADAR_TYPE(radar_type) for radar_type in IDR_DATA[base]["radar_types"]
        }
        assert radar_location.__doc__ == IDR_DATA[base]["doc"]
        assert radar_location.location[0] == IDR_DATA[base]["latitude"]
        assert radar_location.location[1] == IDR_DATA[base]["longitude"]
