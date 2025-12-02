from dataclasses import dataclass
from typing import Optional
from pure_protobuf.annotations import Field
from typing import Annotated

from pure_protobuf.message import BaseMessage


@dataclass(frozen=True)
class RadarFrameModel(BaseMessage):

    frame_id: Annotated[str, Field(1)]
    frame_height: Annotated[int, Field(2)]
    frame_width: Annotated[int, Field(3)]
    data: Annotated[bytes, Field(4)]
    locale_tz: Annotated[Optional[str], Field(5)] = None
