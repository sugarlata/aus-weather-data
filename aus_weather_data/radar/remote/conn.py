import ftplib
import logging
import threading

from io import BytesIO

from ..common.file_handling.remote import BOMRadarPNGRemoteFile
from aus_weather_data.core.logger import (
    log,
    LOG_FORMAT,
    GLOBAL_LOG_LEVEL,
    GLOBAL_LOG_FILE,
    GLOBAL_LOG_STREAM,
)

from aus_weather_data.radar.common.constants import (
    BOM_FTP_HOST,
    BOM_FTP_USER,
    BOM_FTP_PASS,
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

        try:
            self._keep_alive_thread.cancel()
            self._keep_alive_thread = None
        except Exception as e:
            logger.exception(e)

        try:
            self._ftp_conn.quit()
            self._ftp_conn = None
        except Exception as e:
            logger.exception(e)
            self._ftp_conn = None

    def _keep_alive(self):
        """
        Keep the FTP connection alive
        """

        try:
            self._ftp_conn.pwd()
        except Exception as e:
            logger.exception(e)

    def get_directory_contents(self, directory: str) -> list[str]:
        """Get the contents of the given directory.

        Args:
            directory: The directory to get the contents of.

        Returns:
            A list of filenames in the given directory.
        """

        try:
            return self._ftp_conn.nlst(directory)
        except Exception as e:
            logger.exception(e)
            return []

    def get_file(self, remote_file: BOMRadarPNGRemoteFile) -> BOMRadarPNGRemoteFile:
        """Get the contents of the given file.

        Args:
            filename: The filename to get the contents of.

        Returns:
            The contents of the given file.
        """

        try:
            byte_stream = BytesIO()
            self._ftp_conn.retrbinary(
                f"RETR {remote_file.full_path}", byte_stream.write
            )
            remote_file.data = byte_stream.getvalue()
            return remote_file

        except Exception as e:
            logger.exception(e)
            return None
