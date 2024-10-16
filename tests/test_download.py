import datetime

from aus_weather_data.radar.common.location import BOMRadarLocation
from aus_weather_data.radar.remote.download import BOMRadarDownload, RADAR_TYPE
from .constants import TEST_WITH_CONNECTION


def test_download():

    if not TEST_WITH_CONNECTION:
        return

    radar_download = BOMRadarDownload()

    with radar_download:
        radar_download.get_radar_frames(
            BOMRadarLocation.IDR02,
            RADAR_TYPE.REF_128_KM,
            datetime.datetime.now(tz=datetime.timezone.utc)
            - datetime.timedelta(hours=2),
            datetime.datetime.now(tz=datetime.timezone.utc),
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
