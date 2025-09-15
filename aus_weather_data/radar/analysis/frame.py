import os
import pytz
import zlib
import pickle

from typing import Optional
from aus_weather_data.models import IntensityArrays, DiscreteCells
from aus_weather_data.radar.common.frame import BOMRadarFrameBase


class BOMRadarFrameAnalysis(BOMRadarFrameBase):

    filename: str
    frame_id: str
    intensity_arrays: IntensityArrays
    discrete_cells: DiscreteCells

    def __init__(
        self,
        filepath: Optional[str] = None,
        serialized_analysis_data: Optional[bytes] = None,
        locale_tz: Optional[pytz.BaseTzInfo] = None,
    ):
        png_filename = f"{os.path.splitext(os.path.basename(filepath))[0]}.png"
        super().__init__(filename=png_filename, locale_tz=locale_tz)

        if filepath is not None:
            return self._load_from_file(filepath)

        if serialized_analysis_data is not None:
            return self._load_from_binary_data(serialized_analysis_data)

        raise ValueError("Either filename or analysis_binary_data must be provided.")

    def _load_from_file(self, filepath: str):

        with open(filepath, "rb") as file:
            serialized_analysis_data = file.read()

        self._load_from_binary_data(serialized_analysis_data)

    def _load_from_binary_data(self, serialized_analysis_data: bytes):

        data = pickle.loads(serialized_analysis_data)

        self._filename = data["filename"]
        self._frame_id = data["frame_id"]
        self.intensity_arrays = pickle.loads(zlib.decompress(data["intensity_arrays"]))
        self.discrete_cells = pickle.loads(zlib.decompress(data["discrete_cells"]))

    def __str__(self):
        return f"BOMRadarFrameAnalysis<frame_id={self.frame_id}>"

    def __repr__(self):
        return self.__str__()
