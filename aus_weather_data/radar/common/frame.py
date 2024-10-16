import os
import pytz
import datetime

from typing import Optional, Union

from aus_weather_data.radar.common.utils import split_filename
from aus_weather_data.radar.common.location import (
    BOMRadarLocation,
    BOMRadarLocationModel,
)
from aus_weather_data.radar.common.types import RADAR_TYPE
from aus_weather_data.exceptions import ParseFrameError


class __BOMRadarFrameBase(object):
    """Radar Frame object for data from BOM.

    This is a base class to hold metadata related to a radar frame. See
    documentation for the functions in this class.

    Start time covers the start of the time range that this frame
    covers. End time is end of the time range that this frame covers.
    This value needs to be set after instantiation. Generally speaking
    this value is the start_time of the next frame in the sequence.
    Both start_time and end_time should be localized to UTC locale.

    Locale dependent function will return according to the locale if
    set in locale_tz. If locale_tz is not set, defaults to UTC locale.

    Attributes:
        locale_tz: Timezone for locale functions.
        start_time: Start time of the frame. Auto populates from the date time extracted from the filename.
        end_time: End time of the frame - generally start_time of the next frame in a sequence.
    """

    locale_tz: Optional[pytz.BaseTzInfo]
    start_time: datetime.datetime
    end_time: datetime.datetime

    def __init__(
        self,
        filename: str,
        locale_tz: Optional[pytz.BaseTzInfo] = None,
    ):
        """Initialize the BOMRadarFrameBase class

        This will create a RadarFrameBase object.

        Args:
            data: Either :class:`LocalBOMRadarFile` or :class:`RemoteBOMRadarFile` to load.
            locale_tz (optional): :class:`pytz.timezone` object passed for localizing datetime object.
        """

        self._filename: str = filename
        self._metadata: dict = split_filename(self._filename)
        self.start_time = self._metadata["dt"]
        self.locale_tz = locale_tz

        try:
            getattr(BOMRadarLocation, self.radar_id_str)
        except AttributeError:
            raise ParseFrameError(
                f"Could not parse {filename} (Couldn't match location)"
            )

        try:
            RADAR_TYPE(self.radar_type_str)
        except ValueError:
            raise ParseFrameError(
                f"Could not parse {filename} (Couldn't match Radar Type)"
            )

    def __str__(self):
        return f"BOMRadarFrame<filename={self._filename}>"

    def __repr__(self):
        return self.__str__()

    @property
    def radar_id_str(self) -> str:
        """IDR extracted from the filename. EG. :literal:`IDR02` for Melbourne"""

        return str(self._metadata["idr"])

    @property
    def radar_id(self) -> BOMRadarLocationModel:
        """Returns the radar ID as a :class:`BOMRadarLocation` object"""

        return getattr(BOMRadarLocation, self.radar_id_str)  # type: ignore[no-any-return]

    @property
    def radar_type_str(self) -> str:
        """IDR type extracted from the filename. EG. :literal:`3` for 128km Reflectivity"""

        return str(self._metadata["idrType"])

    @property
    def radar_type(self) -> RADAR_TYPE:
        """Returns the radar type as a :class:`RADAR_TYPE` object"""

        return RADAR_TYPE(self.radar_type_str)

    @property
    def radar_base_str(self) -> str:
        """Base extracted from the filename. EG. :literal:`IDR023` for Melbourne 128km Reflectivity"""

        return str(self._metadata["base"])

    @property
    def epoch_time(self) -> float:
        """Seconds since epoch for the start of the frame."""

        return self.dt_utc.timestamp()

    @property
    def dt_utc(self) -> datetime.datetime:
        """Datetime object that is timezone aware for UTC locale."""
        return self._metadata["dt"]  # type: ignore[no-any-return]

    @property
    def dt_locale(self) -> datetime.datetime:
        """Datetime object that is timezone aware for `locale_tz` locale. If locale_tz is None (default), then uses UTC locale."""

        if self.locale_tz:
            return self.dt_utc.astimezone(self.locale_tz)
        else:
            return self.dt_utc

    @property
    def year_utc(self) -> str:
        """Year in UTC timezone (YYYY)."""
        return str(self._metadata["year"])

    @property
    def year_locale(self) -> str:
        """Year in locale timezone (YYYY)."""

        return self.dt_locale.strftime("%Y")

    @property
    def month_utc(self) -> str:
        """Month in UTC timezone (MM)."""
        return str(self._metadata["month"])

    @property
    def month_locale(self) -> str:
        """Month in locale timezone (MM)."""

        return self.dt_locale.strftime("%m")

    @property
    def day_utc(self) -> str:
        """Day in UTC timezone (DD)."""
        return str(self._metadata["day"])

    @property
    def day_locale(self) -> str:
        """Day in locale timezone (DD)."""

        return self.dt_locale.strftime("%d")

    @property
    def hour_utc(self) -> str:
        """Hour in UTC timezone (HH)."""
        return str(self._metadata["hour"])

    @property
    def hour_locale(self) -> str:
        """Hour in locale timezone (HH)."""

        return self.dt_locale.strftime("%H")

    @property
    def minute_utc(self) -> str:
        """Minute in UTC timezone (MM)."""
        return str(self._metadata["minute"])

    @property
    def minute_locale(self) -> str:
        """Minute in locale timezone (MM)."""

        return self.dt_locale.strftime("%M")

    @property
    def date_utc(self) -> str:
        """UTC date string (YYYY-MM-DD)."""
        return str(self._metadata["date"])

    @property
    def date_locale(self) -> str:
        """Locale date string (YYYY-MM-DD)"""
        return self.dt_locale.strftime("%Y-%m-%d")

    @property
    def nice_date_utc(self) -> str:
        """UTC date string fit for human consumption"""

        return self.dt_utc.strftime("%Y-%m-%d %H:%M UTC")

    @property
    def nice_date_locale(self) -> str:
        """Locale date string fit for human consumption"""

        if self.locale_tz:
            return self.dt_locale.strftime(f"%Y-%m-%d %H:%M {self.locale_tz.zone}")
        else:
            return self.nice_date_utc

    @property
    def filename(self) -> str:
        """Filename of the frame"""

        return self._filename


class BOMRadarFrameMetadata(__BOMRadarFrameBase):
    """Radar Frame object for data from BOM.

    This is a class to hold metadata related to a radar frame. See
    documentation for the functions in this class.

    It is a public implementation of :class:`__BOMRadarFrameBase`.

    """

    pass


class BOMRadarFramePNG(__BOMRadarFrameBase):
    """Radar Frame object for data from BOM.

    This is a class to hold metadata and radar data. See
    documentation for the functions in this class.

    It is a public implementation of :class:`__BOMRadarFrameBase`.

    """

    _png_data: Union[bytes, None]

    def load_png_data(self, data: bytes):
        """Load PNG data from a byte string

        Args:
            data: PNG data as a byte string

        """

        self._png_data = data

    def load_png_from_file(self, path: str):
        """Load PNG data from a file

        Args:
            path: Path to the file

        """

        with open(os.path.join(path, self.filename), "rb") as f:
            self._png_data = f.read()

    def save_png_to_file(self, path: str):
        """Save PNG data to a file

        Args:
            path: Path to the file

        """

        if not self._png_data:
            raise ValueError("self._png_data is None")

        with open(os.path.join(path, self.filename), "wb") as f:
            f.write(self._png_data)

    @property
    def png_data(self) -> bytes:
        """Get the PNG data

        Returns:
            (bytes): PNG data as a byte string

        """
        if self._png_data is None:
            raise ValueError("self._png_data is None")
        return self._png_data


class BOMRadarFrameData(BOMRadarFramePNG):
    """Radar Frame object for data from BOM.

    This is a class to hold metadata and radar data in a binary format.
    See documentation for the functions in this class.

    It extends :class:`BOMRadarFramePNG`.

    (Current wip)

    """

    pass


__all__ = [
    "BOMRadarFrameMetadata",
    "BOMRadarFramePNG",
    "BOMRadarFrameData",
]
