import os
import sys
import pytz
import base64
import datetime

from aus_weather_data import BOMRadarFramePNG, BOMRadarPNGLocalFile

# TODO Need to add in a test case here for difference between UTC year and locale year.


def test_file_load():
    filename_base = "IDR024.T.202001312324"
    path = os.path.join(*[".", "tests", "assets"])

    local_file = BOMRadarPNGLocalFile(f"{filename_base}.png", path)

    local_file.load_data_from_file()

    frame = BOMRadarFramePNG(local_file)

    with open(os.path.join(*[path, f"{filename_base}.b64"])) as f:
        b64_data = f.read()
        assert frame.data == base64.b64decode(b64_data)


def test_file_save():
    filename_base = "IDR024.T.202001312324"

    path = os.path.join(*[".", "tests", "assets"])

    local_file = BOMRadarPNGLocalFile(f"{filename_base}.png", path)

    local_file.load_data_from_file()

    frame = BOMRadarFramePNG(local_file)

    local_file_output = frame.get_local_file(os.path.join(*[path, "temp"]))

    local_file_output.save_file()

    with open(os.path.join(*[path, "temp", f"{filename_base}.png"]), "rb") as f:
        hex_data = f.read()
        assert frame.data == hex_data

    # Cleanup
    try:
        os.remove(os.path.join(*[path, "temp", f"{filename_base}.png"]))
    except Exception:
        pass


def test_radar_metadata():
    filename_base = "IDR024.T.202001312324"

    path = os.path.join(*[".", "tests", "assets"])

    local_file = BOMRadarPNGLocalFile(f"{filename_base}.png", path)

    local_file.load_data_from_file()

    frame = BOMRadarFramePNG(local_file)

    timezone = pytz.timezone("Australia/Melbourne")
    frame.tz = timezone

    assert frame.radar_id == "IDR02"
    assert frame.radar_type == "4"
    assert frame.radar_id_type == "IDR024"

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
