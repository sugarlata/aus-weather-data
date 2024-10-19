import time
import datetime

from typing import Optional, List, Dict
from loguru import logger

from pytz import BaseTzInfo
from concurrent.futures import ThreadPoolExecutor

from aus_weather_data.radar.common.types import RADAR_TYPE
from aus_weather_data.radar.common.location import BOMRadarLocationModel
from aus_weather_data.radar.common.frame import BOMRadarFramePNG, BOMRadarFrameMetadata
from aus_weather_data.radar.remote.pool import BOMFTPPool
from aus_weather_data.radar.remote.utils import get_matching_files


class BOMRadarDownload(BOMFTPPool):

    _progress = {"total": 0, "current": 0}

    def __init__(self, connections_count: int = 10) -> None:
        """
        Initiate the Radar Download FTP connection.
        """
        self._connections_count = connections_count
        super().__init__(connections=connections_count)

    def get_radar_frames(
        self,
        radar_locations: Optional[List[BOMRadarLocationModel]] = None,
        radar_types: Optional[List[RADAR_TYPE]] = None,
        start_time: Optional[datetime.datetime] = None,
        end_time: Optional[datetime.datetime] = None,
        ignore_list: Optional[List[str]] = None,
    ) -> Dict[BOMRadarLocationModel, Dict[RADAR_TYPE, List[BOMRadarFramePNG]]]:
        """Download radar data for the given radar and time range.

        Args:
            radar_locations: The list of radar locations to download data for. Defaults to None which downloads all radar locations.
            radar_types: The list of radar types to download data for. Defaults to None which downloads all radar types.
            start_time: The start time of the data to download. Defaults to None which downloads all frames on the server.
            end_time: The end time of the data to download. Defaults to None which downloads all frames on the server.
            ignore_list: List of radar frames to ignore. Defaults to None which doesn't ignore any frames.

        Returns:
            A dict :class:`BOMRadarFrameRaw` objects nested by :class:`BOMRadarLocation` and :class:`RADAR_TYPE`.
        """

        logger.debug("Starting radar download")

        # Recast radar_locations and radar_types as lists if they are not already
        if radar_locations and not isinstance(radar_locations, list):
            radar_locations = [radar_locations]

        if radar_types and not isinstance(radar_types, list):
            radar_types = [radar_types]

        # Get all files, only need single connection
        conn = None
        while conn is None:
            try:
                conn = self.get_connection()
            except Exception:
                logger.error("Failed to get connection. Sleeping for 2 seconds.")
                time.sleep(2)

        radar_dir_files = conn.get_directory_contents()
        self.release_connection(conn)

        # Get matching files
        matching_filenames = get_matching_files(
            radar_dir_files,
            radar_locations=radar_locations,
            radar_types=radar_types,
            start_time_utc=start_time,
            end_time_utc=end_time,
            ignore_list=ignore_list,
        )

        all_frames = self._get_frames(matching_filenames)
        frames_map: Dict[
            BOMRadarLocationModel, Dict[RADAR_TYPE, List[BOMRadarFramePNG]]
        ] = {}

        for frame in all_frames:
            frames_map.setdefault(frame.radar_id, {}).setdefault(
                frame.radar_type, []
            ).append(frame)

        return frames_map

    def _get_frame(
        self, remote_file: BOMRadarFrameMetadata, tz: Optional[BaseTzInfo] = None
    ) -> BOMRadarFramePNG:
        """Download a radar frame"""

        conn = None
        while conn is None:
            try:
                conn = self.get_connection()
            except Exception:
                logger.error("Failed to get connection. Sleeping for 2 seconds.")
                time.sleep(2)

        frame = conn.get_file(remote_file)
        self.release_connection(conn)

        self._progress["current"] += 1
        logger.debug(
            f"Downloaded {self._progress['current']}/{self._progress['total']}"
        )

        return frame

    def _get_frames(
        self, remote_files: List[BOMRadarFrameMetadata]
    ) -> List[BOMRadarFramePNG]:
        results = []
        self._progress["current"] = 0
        self._progress["total"] = len(remote_files)

        with ThreadPoolExecutor(max_workers=self._connections_count) as executor:
            results = list(executor.map(self._get_frame, remote_files))

        return results


__all__ = [
    "BOMRadarDownload",
]
