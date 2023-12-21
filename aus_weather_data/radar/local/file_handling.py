import os
import logging

from typing import Union

from aus_weather_data.radar.common import BOMRadarPNGFile

from aus_weather_data.core.logger import (
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


class BOMRadarPNGLocalFile(BOMRadarPNGFile):
    """Class to read and write local BOM radar files."""

    def __init__(self, filename: str, path: Union[str, None] = None):
        """Initialize the LocalBOMRadarFile class.

        Args:
            filename: The filename of the radar frame.
            path: The path to the radar frame.
        """

        super(BOMRadarPNGLocalFile, self).__init__(filename, path)

    @property
    def full_path(self) -> str:
        """Return the full path of the radar file.

        Returns:
            The full path of the radar file.
        """

        if self.path:
            return os.path.join(self.path, self.filename)
        else:
            return self.filename

    def load_data_from_file(self) -> bytes:
        """Open the radar file.

        Returns:
            The contents of the radar file.
        """

        if self.path:
            filename = os.path.join(self.path, self.filename)
        else:
            filename = self.filename

        try:
            with open(filename, "rb") as f:
                self.data = f.read()
        except Exception as e:
            logger.exception(e)
            raise IOError(f"Unable to open file: {filename}")

    def save_file(self) -> None:
        """Save the radar file.

        Args:
            path: The path to save the radar file to.
        """

        if not self.data:
            raise ValueError("No data to save.")

        try:
            with open(self.full_path, "wb") as f:
                f.write(self.data)
        except Exception as e:
            logger.exception(e)
            raise IOError(f"Unable to save file: {self.data}")
