from dataclasses import dataclass, field
from enum import IntEnum
from typing import Annotated, List
from pure_protobuf.annotations import Field
from pure_protobuf.message import BaseMessage

from aus_weather_data.data.models.radar.frame import RadarFrameModel


class RadarIntensityModel(IntEnum):

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


@dataclass(frozen=True)
class StormCellModel(BaseMessage):

    idx: Annotated[int, Field(1)]


@dataclass(frozen=True)
class StormCellBoundingBoxModel(BaseMessage):

    min_row: Annotated[int, Field(1)]
    min_col: Annotated[int, Field(2)]
    max_row: Annotated[int, Field(3)]
    max_col: Annotated[int, Field(4)]


@dataclass(frozen=True)
class StormCellLocationModel(BaseMessage):

    row: Annotated[float, Field(1)]
    col: Annotated[float, Field(2)]


@dataclass(frozen=True)
class StormCellAnalysisModel(BaseMessage):

    intensity: Annotated[RadarIntensityModel, Field(1)]
    cell_id: Annotated[StormCellModel, Field(2)]
    area: Annotated[int, Field(3)]
    area_convex_hull: Annotated[int, Field(4)]
    weight: Annotated[int, Field(5)]
    bbox: Annotated[StormCellBoundingBoxModel, Field(6)]
    centroid: Annotated[StormCellLocationModel, Field(7)]
    centroid_weighted: Annotated[StormCellLocationModel, Field(8)]
    intensity_mean: Annotated[float, Field(9)]
    intensity_max: Annotated[float, Field(10)]


@dataclass(frozen=True)
class RadarFrameAnalysisModel(BaseMessage):

    frame_height: Annotated[int, Field(1)]
    frame_width: Annotated[int, Field(2)]
    frame: Annotated[RadarFrameModel, Field(3)]
    data: Annotated[bytes, Field(4)]
    metadata: Annotated[
        List[StormCellAnalysisModel],
        Field(5),
    ]
