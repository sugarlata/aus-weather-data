from concurrent.futures import ThreadPoolExecutor
import os
import datetime
import logging

from typing import Union

from pytz import BaseTzInfo

from .common import (
    BOM_RADAR_PATH,
    RADAR_TYPE,
    split_filename,
    BOMRadarFramePNG,
    BOMRadarLocationBase,
)

from .remote import BOMFTPConn, BOMFTPPool, BOMRadarPNGRemoteFile

from ..core.logger import (
    log,
    LOG_FORMAT,
    GLOBAL_LOG_LEVEL,
    GLOBAL_LOG_FILE,
    GLOBAL_LOG_STREAM,
)

# Log level for this file. Default pull from global values. Can override here.
LOG_LEVEL = GLOBAL_LOG_LEVEL
LOG_FILE = GLOBAL_LOG_FILE
LOG_STREAM = GLOBAL_LOG_STREAM

# Setup logging for this file
logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
formatter = logging.Formatter(LOG_FORMAT)
file_handler = logging.FileHandler(LOG_FILE)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
if LOG_STREAM:
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)


class BOMRadarDownload(BOMFTPPool):
    def __init__(self) -> None:
        """
        Initiate the Radar Download FTP connection.
        """
        super().__init__()

    @log(logger=logger)
    def get_radar_frames(
        self,
        radar_locations: Union[list[BOMRadarLocationBase], BOMRadarLocationBase] = None,
        radar_types: Union[list[RADAR_TYPE], RADAR_TYPE] = None,
        start_time: datetime.datetime = None,
        end_time: datetime.datetime = None,
        ignore_list: list[str] = None,
    ) -> dict[BOMRadarLocationBase : dict[RADAR_TYPE : list[BOMRadarFramePNG]]]:
        """Download radar data for the given radar and time range.

        Args:
            radar_locations: The list of radar locations to download data for. Defaults to None which downloads all radar locations.
            radar_types: The list of radar types to download data for. Defaults to None which downloads all radar types.
            start_time: The start time of the data to download. Defaults to None which downloads all frames on the server.
            end_time: The end time of the data to download. Defaults to None which downloads all frames on the server.
            ignore_list: List of radar frames to ignore. Defaults to None which doesn't ignore any frames.

        Returns:
            A dict :class:`BOMRadarFrameRaw` objects nested by :class:`BOMRadarLocationBase` and :class:`RADAR_TYPE`.
        """

        # Recast radar_locations and radar_types as lists if they are not already
        if radar_locations and not isinstance(radar_locations, list):
            radar_locations = [radar_locations]

        if radar_types and not isinstance(radar_types, list):
            radar_types = [radar_types]

        # Get all files, only need single connection
        with BOMFTPConn() as conn:
            radar_dir_files = conn.get_directory_contents(BOM_RADAR_PATH)

        # Filter PNG
        filtered_files = [x for x in radar_dir_files if x.endswith(".png")]

        # Get basename
        filtered_files = [os.path.basename(x) for x in filtered_files]

        # Filter for correct length
        filtered_files = [x for x in filtered_files if len(x) == 25]

        # Get matching files
        matching_filenames = self._get_matching_files(
            filtered_files,
            radar_locations=radar_locations,
            radar_types=radar_types,
            start_time=start_time,
            end_time=end_time,
            ignore_list=ignore_list,
        )

        # Convert to Remote Files
        matching_filenames = [
            BOMRadarPNGRemoteFile(x, BOM_RADAR_PATH) for x in matching_filenames
        ]

        frames: list = self._get_frames(matching_filenames)

        # breakpoint()

    @log(logger=logger)
    def _get_matching_files(
        self,
        png_list: list[str],
        radar_locations: list[BOMRadarLocationBase] = None,
        radar_types: list[RADAR_TYPE] = None,
        start_time: datetime.datetime = None,
        end_time: datetime.datetime = None,
        ignore_list: list[str] = None,
    ) -> list[str]:
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

        # Filter through ignore list. Expecting ignore list ot be larger than file_list_metadata
        if ignore_list:
            ignore_set = set(ignore_list)
            png_set = set(png_list)

            filtered_list = list(png_set.difference(ignore_set))
        else:
            filtered_list = png_list

        # Convert to metadata format.
        filtered_list = [split_filename(x) for x in filtered_list]

        # Filter according to radar_type
        if radar_locations:
            radar_locations_str = [x.base() for x in radar_locations]
            filtered_list = [
                x for x in filtered_list if x["idr"] in radar_locations_str
            ]

        # Filter according to radar type
        if radar_types:
            radar_types_str = [x.value for x in radar_types]
            filtered_list = [
                x for x in filtered_list if x["idrType"] in radar_types_str
            ]

        # Filter according to start and end times
        if start_time and end_time:
            filtered_list = [
                x for x in filtered_list if start_time <= x.get("dt") <= end_time
            ]
        elif start_time:
            filtered_list = [x for x in filtered_list if start_time <= x.get("dt")]
        elif end_time:
            filtered_list = [x for x in filtered_list if x.get("dt") <= end_time]

        # Return just filenames
        return [x["filename"] for x in filtered_list]

    def _get_frame(self, remote_file: BOMRadarPNGRemoteFile, tz: BaseTzInfo = None):
        """Download a radar frame"""

        try:
            conn = self.get_connection()
            remote_file = conn.get_file(remote_file)
            self.release_connection(conn)
            return BOMRadarFramePNG(remote_file, tz)
        except Exception as e:
            print(e)
            pass

        return None

    def _get_frames(self, remote_files: list[BOMRadarPNGRemoteFile]):
        results = []
        with self as conn_pool:
            with ThreadPoolExecutor(max_workers=self._connections_count) as executor:
                results = list(executor.map(self._get_frame, remote_files))

        return results


__all__ = [BOMRadarDownload]
