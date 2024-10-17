import pytest
from .constants import ANON_GEN_RADAR_DIRECTORY_TEST_FILES
from aus_weather_data.radar.common.location import BOMRadarLocation
from aus_weather_data.radar.common.types import RADAR_TYPE


@pytest.mark.parametrize(
    "radar_location, radar_type",
    [
        (getattr(BOMRadarLocation, radar_location), radar_type)
        for radar_location in BOMRadarLocation.IDR_LIST
        for radar_type in [t for t in RADAR_TYPE]
    ],
)
def test_matching_files_normal(radar_location, radar_type):

    from aus_weather_data.radar.remote.utils import get_matching_files

    matching_files = get_matching_files(
        ANON_GEN_RADAR_DIRECTORY_TEST_FILES,
        [radar_location],
        [radar_type],
    )

    for metadata in matching_files:
        assert metadata.radar_id == radar_location
        assert metadata.radar_type == radar_type
