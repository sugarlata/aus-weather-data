from dataclasses import dataclass
from enum import Enum
import numpy as np

from aus_weather_data.domain.entities.radar.frame import RadarFrame


class RadarIntensity(Enum):

    INTENSITY_0 = 0
    INTENSITY_1 = 1
    INTENSITY_2 = 2
    INTENSITY_3 = 3
    INTENSITY_4 = 4
    INTENSITY_5 = 5
    INTENSITY_6 = 6
    INTENSITY_7 = 7
    INTENSITY_8 = 8
    INTENSITY_9 = 9
    INTENSITY_10 = 10
    INTENSITY_11 = 11
    INTENSITY_12 = 12
    INTENSITY_13 = 13
    INTENSITY_14 = 14
    INTENSITY_15 = 15

    @property
    def binary_mask_layer(self) -> int:
        return self.value - 1

    @property
    def cell_identification_layer(self) -> int:
        return self.value - 1 + 15


@dataclass(frozen=True)
class StormCell:
    idx: int


@dataclass(frozen=True)
class StormCellBoundingBox:
    min_row: int
    min_col: int
    max_row: int
    max_col: int


@dataclass(frozen=True)
class AnalysisLocation:
    row: float
    col: float


@dataclass(frozen=True)
class StormCellAnalysis:

    intensity: RadarIntensity
    cell_id: StormCell
    area: int
    area_convex_hull: int
    weight: int

    bbox: StormCellBoundingBox

    centroid: AnalysisLocation
    centroid_weighted: AnalysisLocation

    intensity_mean: float
    intensity_max: float


@dataclass(frozen=True)
class RadarFrameAnalysis:

    frame_shape: tuple[int, int]
    frame: RadarFrame

    # Analysis data
    data: np.ndarray
    metadata: dict[RadarIntensity, dict[StormCell, StormCellAnalysis]]

    def __str__(self):
        return f"RadarFrameAnalysis<filename={self.frame.frame_id}>"

    def __repr__(self):
        return self.__str__()
