import os
import datetime

from loguru import logger
from typing import List, Union, Optional

from aus_weather_data.exceptions import ParseFrameError
from aus_weather_data.radar.common.types import RADAR_TYPE
from aus_weather_data.radar.common.location import BOMRadarLocationModel
from aus_weather_data.radar.common.frame import BOMRadarFrameMetadata


def __convert_to_metadata(filename: str) -> Union[BOMRadarFrameMetadata, None]:

    try:
        return BOMRadarFrameMetadata(filename)
    except ParseFrameError:
        logger.debug(f"Failed to parse frame: {filename}. Skipping")
        return None


def get_matching_files(
    file_list: List[str],
    radar_locations: Optional[List[BOMRadarLocationModel]] = None,
    radar_types: Optional[List[RADAR_TYPE]] = None,
    start_time_utc: Optional[datetime.datetime] = None,
    end_time_utc: Optional[datetime.datetime] = None,
    ignore_list: Optional[List[str]] = None,
) -> List[BOMRadarFrameMetadata]:
    """Get a list of matching files for the given radars, radar_types and time range.

    Args:
        file_list: List of files to match against (should be just the basename).
        radar_locations: The radar(s) to download data for.
        radar_types: The radar types to download.
        start_time: The start time of the data to download.
        end_time: The end time of the data to download.
        ignore_list: radar frames to ignore (should be just the basename).

    Returns:
        A list of matching filenames.
    """

    logger.info("Filtering radar files")

    # Filter PNG
    filtered_files = [x for x in file_list if x.endswith(".png")]

    # Get basename
    filtered_files = [os.path.basename(x) for x in filtered_files]

    # Filter for correct length
    filtered_files = [x for x in filtered_files if len(x) == 25 or len(x) == 26]

    # Filter through ignore list. Expecting ignore list ot be larger than file_list_metadata
    if ignore_list:
        ignore_set = set(ignore_list)
        png_set = set(filtered_files)
        filtered_files = list(png_set.difference(ignore_set))

    # Convert to metadata format.
    metadata: List[BOMRadarFrameMetadata] = [
        metadataFrame
        for x in filtered_files
        if (metadataFrame := __convert_to_metadata(x)) is not None
    ]

    # Filter according to radar_type
    if radar_locations:
        metadata = [x for x in metadata if x.radar_id in radar_locations]

    # Filter according to radar type
    if radar_types:
        metadata = [x for x in metadata if x.radar_type in radar_types]

    # Filter according to start and end times
    if start_time_utc and end_time_utc:
        metadata = [x for x in metadata if start_time_utc <= x.dt_utc <= end_time_utc]
    elif start_time_utc:
        metadata = [x for x in metadata if start_time_utc <= x.dt_utc]
    elif end_time_utc:
        metadata = [x for x in metadata if x.dt_utc <= end_time_utc]

    # Return just filenames
    return metadata


__all__ = [
    "get_matching_files",
]
