import os
import time
import pytz
import datetime
from aus_weather_data.radar.common.utils import split_filename
from .frame_base import BOMRadarFrameBase
from aus_weather_data.radar.common import BOMRadarFile
from aus_weather_data.radar.local import BOMRadarPNGLocalFile
from typing import Optional


class BOMRadarFramePNG(BOMRadarFrameBase):
    """Radar Frame object for raw PNG data from BOM.

    This is a class to hold metadata and radar data in raw PNG. See
    documentation for the functions in this class.

    Start time covers the start of the time range that this frame
    covers. End time is end of the time range that this frame covers.
    This value needs to be set after instantiation. Generally speaking
    this value is the start_time of the next frame in the sequence.
    Both start_time and end_time should be localized to UTC locale.

    Locale dependent function will return according to the locale if
    set in tz. If tz is not set, defaults to UTC locale.

    Attributes:
        tz: Timezone for locale functions.
        start_time: Start time of the frame. Auto populates from the date time extracted from the filename.
        end_time: End time of the frame - generally start_time of the next frame in a sequence.
    """

    tz: pytz.BaseTzInfo
    start_time: datetime.datetime
    end_time: datetime.datetime

    def __init__(
        self,
        radar_file: BOMRadarFile,
        tz: Optional[pytz.BaseTzInfo] = None,
    ):
        """Initialize the BOMRadarFrameRaw class

        This will create a RadarFrameRaw, data can be of type string  to load
        from a file, in which case data should be the filename. Otherwise data
        should be of type ByteString, which is the raw png data.

        Args:
            data: Either :class:`LocalBOMRadarFile` or :class:`RemoteBOMRadarFile` to load.
            tz (optional): :class:`pytz.timezone` object passed for localizing datetime object.
        """

        super(BOMRadarFramePNG, self).__init__(radar_file.filename, tz)

        self._filename: str = radar_file.filename
        self._metadata: dict = split_filename(self._filename)
        self.start_time = self._metadata["dt"]

        if not radar_file.data:
            raise ValueError("radar_file.data is None")

        self._data: bytes = radar_file.data

        if tz:
            self.tz = tz

    def get_local_file(self, path: str = None) -> BOMRadarPNGLocalFile:
        """Saves the radar frame to a png file

        Args:
            path: local path to assign the file to. If None, will assign to current directory.
        """

        radar_file = BOMRadarPNGLocalFile(self.filename, path)

        radar_file.data = self._data

        return radar_file

    def __str__(self):
        return f"BOMRadarFramePNG<{self._filename}>"

    @property
    def data(self) -> bytes:
        """Binary Data png of the frame"""

        return self._data
