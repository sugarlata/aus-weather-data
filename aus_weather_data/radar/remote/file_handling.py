from typing import Union
from aus_weather_data.radar.common import BOMRadarPNGFile


class BOMRadarPNGRemoteFile(BOMRadarPNGFile):
    """Class to read remote BOM radar files."""

    def __init__(self, filename: str, path: Union[str, None] = None):
        """Initialize the BOMRadarPNGRemoteFile class."""

        super(BOMRadarPNGRemoteFile, self).__init__(filename, path)

    @property
    def full_path(self) -> str:
        """Get the full path to the file.

        Returns:
            The full path to the file.
        """

        if self.path:
            return f"{self.path}/{self.filename}"
        else:
            return self.filename
