import ftplib
import threading

from io import BytesIO
from loguru import logger
from typing import List

from aus_weather_data.radar.common.frame import (
    BOMRadarFrameMetadata,
    BOMRadarFramePNG,
)

from aus_weather_data.constants import (
    BOM_FTP_HOST,
    BOM_FTP_USER,
    BOM_FTP_PASS,
    BOM_RADAR_PATH,
)


class BOMFTPConn(object):
    """
    BOM FTP Connection class

    This is a class to make a single ftp connection to BOM. It can be
    used to download radar frames.
    """

    _ftp_conn: ftplib.FTP
    _keep_alive_thread: threading.Thread
    _file_buffer: None

    def __init__(self) -> None:
        """
        Instantiate the FTP Host connection.
        """
        super(BOMFTPConn, self).__init__()

    def __enter__(self):
        """
        Context Manager for single connection
        """
        self.open_conn()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Exit Context Manager
        """
        self.quit()

    def open_conn(self):
        """
        Login to the server
        """

        self._ftp_conn = ftplib.FTP(BOM_FTP_HOST, BOM_FTP_USER, BOM_FTP_PASS)

        self._ftp_conn.sendcmd("TYPE I")

        # Timer for keep alive
        self._keep_alive_thread = threading.Timer(60.0, self._keep_alive)

    def quit(self):
        """
        Close the FTP connection
        """

        if self._keep_alive_thread:
            self._keep_alive_thread.cancel()
            self._keep_alive_thread = None

        try:
            self._ftp_conn.quit()
            self._ftp_conn = None
        except ftplib.all_errors as e:
            logger.exception(e)
            self._ftp_conn = None

    def _keep_alive(self):
        """
        Keep the FTP connection alive
        """

        try:
            self._ftp_conn.pwd()
        except ftplib.all_errors as e:
            logger.exception(e)

    def get_directory_contents(self, directory: str = BOM_RADAR_PATH) -> List[str]:
        """Get the contents of the given directory.

        Args:
            directory: The directory to get the contents of.

        Returns:
            A list of filenames in the given directory.
        """

        try:
            return self._ftp_conn.nlst(directory)
        except ftplib.all_errors as e:
            logger.exception(e)
            return []

    def get_file(self, remote_file: BOMRadarFrameMetadata) -> BOMRadarFramePNG:
        """Get the contents of the given file.

        Args:
            filename: The filename to get the contents of.

        Returns:
            The contents of the given file as bytes.

        Raises:
            IOError: If the file cannot be retrieved.
        """

        try:
            byte_stream = BytesIO()
            self._ftp_conn.retrbinary(
                f"RETR {BOM_RADAR_PATH}/{remote_file.filename}", byte_stream.write
            )
            png_frame = BOMRadarFramePNG(
                remote_file.filename,
                locale_tz=remote_file.locale_tz,
            )

            png_frame.load_png_data(byte_stream.getvalue())
            return png_frame

        except ftplib.all_errors as e:
            logger.exception(e)
            raise IOError(f"Failed to get file {remote_file.filename} from FTP: {e}")

    def get_files(
        self, remote_files: List[BOMRadarFrameMetadata]
    ) -> List[BOMRadarFramePNG]:
        """Get the contents of the given files.

        Args:
            remote_files: The files to get the contents of.

        Returns:
            The contents of the given files as a list of bytes.

        Raises:
            IOError: If the files cannot be retrieved.
        """

        frames = []

        for remote_file in remote_files:
            try:
                frames.append(self.get_file(remote_file))
            except IOError as e:
                logger.exception(e)

        return frames


__all__ = [
    "BOMFTPConn",
]
