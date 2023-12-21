import datetime

from aus_weather_data import split_filename


def test_split_filename():
    assert split_filename("IDR66A.T.202312132105.png") == {
        "filename": "IDR66A.T.202312132105.png",
        "idr": "IDR66",
        "idrType": "A",
        "idrIdType": "IDR66A",
        "year": "2023",
        "month": "12",
        "day": "13",
        "hour": "21",
        "minute": "05",
        "date": "2023-12-13",
        "dt": datetime.datetime(
            year=2023, month=12, day=13, hour=21, minute=5, tzinfo=datetime.timezone.utc
        ),
    }

    assert split_filename("IDR00004.T.202312131628.png") == {
        "filename": "IDR00004.T.202312131628.png",
        "idr": "IDR0000",
        "idrType": "4",
        "idrIdType": "IDR00004",
        "year": "2023",
        "month": "12",
        "day": "13",
        "hour": "16",
        "minute": "28",
        "date": "2023-12-13",
        "dt": datetime.datetime(
            year=2023,
            month=12,
            day=13,
            hour=16,
            minute=28,
            tzinfo=datetime.timezone.utc,
        ),
    }
