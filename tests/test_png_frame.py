import os
import pytz
import datetime
import tempfile

from aus_weather_data.radar.common.frame import BOMRadarFramePNG
from aus_weather_data.radar.common.location import BOMRadarLocation
from aus_weather_data.radar.common.types import RADAR_TYPE


def test_file_load_and_save():
    filename_base = "IDR024.T.202001312324"
    path = os.path.join(*[".", "tests", "assets"])

    frame = BOMRadarFramePNG(f"{filename_base}.png")
    frame.load_png_from_file(path)

    tmp = tempfile.TemporaryDirectory()

    frame.save_png_to_file(tmp.name)

    with open(os.path.join(*[tmp.name, f"{filename_base}.png"]), "rb") as f:
        hex_data = f.read()
        assert frame._png_data == hex_data

    tmp.cleanup()




def test_radar_metadata():
    filename_base = "IDR024.T.202001312324"
    timezone = pytz.timezone("Australia/Melbourne")
    frame = BOMRadarFramePNG(f"{filename_base}.png", timezone)


    assert frame.radar_id_str == "IDR02"
    assert frame.radar_type_str == "4"
    assert frame.radar_base_str == "IDR024"

    assert frame.radar_id == BOMRadarLocation.IDR02
    assert frame.radar_type == RADAR_TYPE.REF_64_KM

    assert frame.dt_utc == datetime.datetime(
        2020, 1, 31, 23, 24, 0, 0, datetime.timezone.utc
    )

    assert frame.dt_locale == datetime.datetime(
        2020, 1, 31, 23, 24, 0, 0, datetime.timezone.utc
    ).astimezone(timezone)

    assert frame.year_utc == "2020"
    assert frame.month_utc == "01"
    assert frame.day_utc == "31"
    assert frame.hour_utc == "23"
    assert frame.minute_utc == "24"

    assert frame.year_locale == "2020"
    assert frame.month_locale == "02"
    assert frame.day_locale == "01"
    assert frame.hour_locale == "10"
    assert frame.minute_locale == "24"

    assert frame.date_utc == "2020-01-31"
    assert frame.date_locale == "2020-02-01"

    assert frame.nice_date_utc == "2020-01-31 23:24 UTC"
    assert frame.nice_date_locale == "2020-02-01 10:24 Australia/Melbourne"

    assert frame.filename == f"{filename_base}.png"
