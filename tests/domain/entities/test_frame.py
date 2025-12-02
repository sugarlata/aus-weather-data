import pytest
import datetime


@pytest.mark.parametrize(
    "frame_id, radar_id, radar_type_str, radar_base, year, month, day, hour, minute",
    [
        (
            "IDR024.T.202001312324",
            "IDR02",
            "4",
            "IDR024",
            "2020",
            "01",
            "31",
            "23",
            "24",
        ),
        (
            "IDR1004.T.202001312324",
            "IDR100",
            "4",
            "IDR1004",
            "2020",
            "01",
            "31",
            "23",
            "24",
        ),
    ],
)
def test_frame_metadata_success(
    frame_id: str,
    radar_id: str,
    radar_type_str: str,
    radar_base: str,
    year: str,
    month: str,
    day: str,
    hour: str,
    minute: str,
):
    from aus_weather_data.domain.entities.radar.frame import RadarFrameMetadata

    metadata = RadarFrameMetadata(frame_id)

    assert metadata.radar_id == radar_id
    assert metadata.radar_type_str == radar_type_str
    assert metadata.radar_base == radar_base
    assert metadata.year == year
    assert metadata.month == month
    assert metadata.day == day
    assert metadata.hour == hour
    assert metadata.minute == minute
    assert metadata.date == f"{year}-{month}-{day}"
    assert metadata.dt == datetime.datetime(
        int(year),
        int(month),
        int(day),
        int(hour),
        int(minute),
        tzinfo=datetime.timezone.utc,
    )


@pytest.mark.parametrize(
    "frame_id",
    [
        "IDR024.T.202001312324.png",
        "IDR05524.T.202001312324",
        "IDR024.T.2020013123244",
        "IDR024.202001312324.png",
    ],
)
def test_frame_metadata_failure(
    frame_id: str,
):
    from aus_weather_data.domain.entities.radar.frame import RadarFrameMetadata

    with pytest.raises(ValueError):
        RadarFrameMetadata(frame_id)
