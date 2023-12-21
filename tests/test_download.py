import os
import sys
import pytz
import base64
import datetime

from aus_weather_data import BOMRadarDownload, BOMRadarLocation, RADAR_TYPE


def test_download():
    radar_download = BOMRadarDownload()

    with radar_download:
        radar_download.get_radar_frames(
            BOMRadarLocation.IDR02,
            RADAR_TYPE.REF_128_KM,
            datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
            - datetime.timedelta(minutes=30),
            datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc),
            [
                "IDR98I.T.202312132024.png",
                "IDR98I.T.202312132029.png",
                "IDR98I.T.202312132034.png",
                "IDR98I.T.202312132039.png",
                "IDR98I.T.202312132044.png",
                "IDR98I.T.202312132049.png",
                "IDR98I.T.202312132054.png",
                "IDR98I.T.202312132059.png",
                "IDR98I.T.202312132104.png",
                "IDR98I.T.202312132109.png",
                "IDR98I.T.202312132114.png",
                "IDR98I.T.202312132119.png",
            ],
        )
