import os
import sys
import base64
import datetime
from zoneinfo import ZoneInfo

if True:
    sys.path.insert(0, os.path.abspath("."))
    from aus_weather_data import BOMRadarFrameRaw

# TODO Need to add in a test case here for difference between UTC year and locale year.


def test_file_load():
    filename_base = 'IDR024.T.202001312324'

    frame = BOMRadarFrameRaw(
        f'{filename_base}.png',
        os.path.join(*[
            '.',
            'tests',
            'assets',
            f'{filename_base}.png'
        ]))

    with open(os.path.join(*[
        '.',
        'tests',
        'assets',
        f'{filename_base}.b64'
    ])) as f:
        b64_data = f.read()
        assert frame.data == base64.b64decode(b64_data)


def test_file_save():
    filename_base = 'IDR024.T.202001312324'

    frame = BOMRadarFrameRaw(
        f'{filename_base}.png',
        os.path.join(*[
            '.',
            'tests',
            'assets',
            f'{filename_base}.png'
        ]))

    frame.save_to_file(os.path.join(*[
        '.',
        'tests',
        'assets',
        f'{filename_base}-output.png'
    ]))

    with open(os.path.join(*[
        '.',
        'tests',
        'assets',
        f'{filename_base}-output.png'
    ]), 'rb') as f:
        hex_data = f.read()
        assert frame.data == hex_data

    # Cleanup
    try:
        os.remove(os.path.join(*[
            '.',
            'tests',
            'assets',
            f'{filename_base}-output.png'
        ]))
    except Exception:
        pass


def test_radar_metadata():
    filename_base = 'IDR024.T.202001312324'

    frame = BOMRadarFrameRaw(
        f'{filename_base}.png',
        os.path.join(*[
            '.',
            'tests',
            'assets',
            f'{filename_base}.png'
        ]))

    frame.tz = ZoneInfo('Australia/Melbourne')

    assert frame.radar_id == "IDR02"
    assert frame.radar_type == "4"
    assert frame.radar_id_type == "IDR024"

    assert frame.dt_utc == datetime.datetime(
        2020, 1, 31, 23, 24, 0, 0, datetime.timezone.utc
    )

    assert frame.dt_locale == datetime.datetime(
        2020, 1, 31, 23, 24, 0, 0, datetime.timezone.utc
    ).astimezone(ZoneInfo('Australia/Melbourne'))

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
