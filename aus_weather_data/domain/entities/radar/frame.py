import re
import pytz
import datetime
import numpy as np

from functools import cached_property
from typing import Optional
from dataclasses import dataclass


@dataclass(frozen=True)
class RadarFrameMetadata:

    frame_id: str

    def __post_init__(self):

        if not re.match(r"^IDR\d{2,4}\.\w\.\d{12}$", self.frame_id):
            raise ValueError("Filename is not in the correct format.")


    @property
    def radar_id(self) -> str:
        return self.frame_id.split(".")[0][:-1]

    @property
    def radar_type_str(self) -> str:
        return self.frame_id.split(".")[0][-1:]

    @property
    def radar_base(self) -> str:
        return self.frame_id.split(".")[0]

    @property
    def year(self) -> str:
        return self.frame_id.split(".")[2][0:4]

    @property
    def month(self) -> str:
        return self.frame_id.split(".")[2][4:6]

    @property
    def day(self) -> str:
        return self.frame_id.split(".")[2][6:8]

    @property
    def hour(self) -> str:
        return self.frame_id.split(".")[2][8:10]

    @property
    def minute(self) -> str:
        return self.frame_id.split(".")[2][10:12]

    @property
    def date(self) -> str:
        return "{year}-{month}-{day}".format(
            year=self.year, month=self.month, day=self.day
        )

    @property
    def dt(self) -> datetime.datetime:
        return datetime.datetime.strptime(
            self.frame_id.split(".")[2], "%Y%m%d%H%M"
        ).replace(tzinfo=datetime.timezone.utc)


@dataclass(frozen=True)
class RadarFrame:
    """Radar Frame object for radar data from BOM."""

    frame_id: str
    frame_shape: tuple[int, int]
    data: np.ndarray
    locale_tz: Optional[pytz.BaseTzInfo] = None

    @cached_property
    def frame_id_metadata(self) -> RadarFrameMetadata:
        return RadarFrameMetadata(self.frame_id)

    @property
    def epoch_time(self) -> float:
        return float(self.frame_id_metadata.dt.timestamp())

    @property
    def dt_locale(self) -> datetime.datetime:

        if self.locale_tz:
            return self.frame_id_metadata.dt.astimezone(self.locale_tz)  # type: ignore
        else:
            raise ValueError("Locale timezone is not set")

    def __str__(self):
        return f"RadarFrame<filename={self.frame_id}>"

    def __repr__(self):
        return self.__str__()
