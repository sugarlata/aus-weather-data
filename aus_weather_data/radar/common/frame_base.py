import pytz
import datetime
from aus_weather_data.radar.common.utils import split_filename
from typing import Optional


class BOMRadarFrameBase:
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
        filename: str,
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

        self._filename: str = filename
        self._metadata: dict = split_filename(self._filename)
        self.start_time = self._metadata["dt"]

        if tz:
            self.tz = tz

    def __str__(self):
        return f"BOMRadarFrame(filename={self._filename})"

    def __repr__(self):
        return self.__str__()

    @property
    def radar_id(self) -> str:
        """IDR extracted from the filename. EG. :literal:`IDR02` for Melbourne"""

        return self._metadata["idr"]

    @property
    def radar_type(self) -> str:
        """IDR type extracted from the filename. EG. :literal:`3` for 128km Reflectivity"""

        return self._metadata["idrType"]

    @property
    def radar_id_type(self) -> str:
        """IDR and Type extracted from the filename. EG. :literal:`IDR023` for Melbourne 128km Reflectivity"""

        return self._metadata["idrIdType"]

    @property
    def epoch_time(self) -> float:
        """Seconds since epoch for the start of the frame."""

        return self.dt_utc.timestamp()

    @property
    def dt_utc(self) -> datetime.datetime:
        """Datetime object that is timezone aware for UTC locale."""
        return self._metadata["dt"]

    @property
    def dt_locale(self) -> datetime.datetime:
        """Datetime object that is timezone aware for `tz` locale. If tz is None (default), then uses UTC locale."""

        if self.tz:
            return self.dt_utc.astimezone(self.tz)
        else:
            return self.dt_utc

    @property
    def year_utc(self) -> str:
        """Year in UTC timezone (YYYY)."""
        return self._metadata["year"]

    @property
    def year_locale(self) -> str:
        """Year in locale timezone (YYYY)."""

        return self.dt_locale.strftime("%Y")

    @property
    def month_utc(self) -> str:
        """Month in UTC timezone (MM)."""
        return self._metadata["month"]

    @property
    def month_locale(self) -> str:
        """Month in locale timezone (MM)."""

        return self.dt_locale.strftime("%m")

    @property
    def day_utc(self) -> str:
        """Day in UTC timezone (DD)."""
        return self._metadata["day"]

    @property
    def day_locale(self) -> str:
        """Day in locale timezone (DD)."""

        return self.dt_locale.strftime("%d")

    @property
    def hour_utc(self) -> str:
        """Hour in UTC timezone (HH)."""
        return self._metadata["hour"]

    @property
    def hour_locale(self) -> str:
        """Hour in locale timezone (HH)."""

        return self.dt_locale.strftime("%H")

    @property
    def minute_utc(self) -> str:
        """Minute in UTC timezone (MM)."""
        return self._metadata["minute"]

    @property
    def minute_locale(self) -> str:
        """Minute in locale timezone (MM)."""

        return self.dt_locale.strftime("%M")

    @property
    def date_utc(self) -> str:
        """UTC date string (YYYY-MM-DD)."""
        return self._metadata["date"]

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

        if self.tz:
            return self.dt_locale.strftime(f"%Y-%m-%d %H:%M {self.tz.zone}")
        else:
            return self.nice_date_utc

    @property
    def filename(self) -> str:
        """Filename of the frame"""

        return self._filename
