import os
import time
from aus_weather_data.utils.funcs import split_filename


class BOMRadarFrame:

    def __init__(self, filename):

        self._filename = filename
        self._metadata = split_filename(filename)
        self._url = f'http://www.bom.gov.au/radar/{filename}'

    def __str__(self):
        return f'BOMRadarFrame(filename={self._filename})'

    def __repr__(self):
        return self.__str__()

    @property
    def radar_id(self):
        return self._metadata["idr"]

    @property
    def radar_type(self):
        return self._metadata["idrType"]

    @property
    def radar_id_type(self):
        return self._metadata["idrIdType"]

    @property
    def year(self):
        return self._metadata["year"]

    @property
    def month(self):
        return self._metadata["month"]

    @property
    def day(self):
        return self._metadata["day"]

    @property
    def hour(self):
        return self._metadata["hour"]

    @property
    def minute(self):
        return self._metadata["minute"]

    @property
    def date(self):
        return self._metadata["date"]

    @property
    def dt(self):
        return self._metadata["dt"]

    @property
    def start_time(self):
        return self._metadata["dt"]

    @property
    def end_time(self):
        return self._metadata.get("end_time")

    @property
    def nice_name(self):
        return '{year}-{month}-{day} {hour}:{minute} UTC'.format(
            year=self.year,
            month=self.month,
            day=self.day,
            hour=self.hour,
            minute=self.minute
        )

    @property
    def filename(self):
        return self._filename

    @property
    def url(self):
        return self._url

    def calc_end_time_from_filename(self, next_filename):
        next_metadata = split_filename(next_filename)
        self._metadata["end_time"] = next_metadata["dt"]

    def calc_end_time_from_dt(self, dt):
        self._metadata["end_time"] = dt
