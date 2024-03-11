from typing import Union


class BOMRadarFile(object):
    """Base Class for BOM radar files."""

    def __init__(self, filename: str, path: Union[str, None] = None):
        """Initialize the BOMRadarFile class.

        Args:
            filename: The filename of the radar frame.
            path: The path to the radar frame.
        """

        self.filename = filename
        self.path = path
        self.data = None
