from loguru import logger
from typing import List

from aus_weather_data.radar.remote.conn import BOMFTPConn


class BOMFTPPool(object):
    """
    Pooling for FTP Connections
    """

    _all_connections: List[BOMFTPConn] = []
    _available_connections: List[BOMFTPConn] = []
    _used_connections: List[BOMFTPConn] = []

    def __init__(self, connections: int = 10):
        """
        Instantiate the FTP Connection Pool

        Args:
            connections: Number of connection to create in the pool. Defaults to 10.
        """

        self._connections_count = connections

    def __enter__(self):
        """
        Enter context manager
        """
        self._init_connections()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Exit Context Manager
        """
        self.close_pool()

    def _init_connections(self):
        """
        Initiate the connections.
        """

        self._all_connections = [
            self._create_new_connection() for x in range(0, self._connections_count)
        ]

        self._available_connections = [x for x in self._all_connections]

    def _create_new_connection(self):
        """
        Function to create the connection
        """

        new_conn = BOMFTPConn()
        new_conn.open_conn()

        return new_conn

    def get_connection(self) -> BOMFTPConn:
        """
        Get a connection from the pool
        """

        if len(self._available_connections) == 0:
            raise Exception("No available connections")

        conn = self._available_connections.pop()
        self._used_connections.append(conn)
        return conn

    def release_connection(self, conn: BOMFTPConn):
        """
        Return a connection to the pool
        """

        self._used_connections.remove(conn)
        self._available_connections.append(conn)

    def close_pool(self):
        """
        Close all connections in this pool
        """

        for conn in self._all_connections:
            try:
                self._close_connection(conn)
            except Exception as e:
                logger.exception(e)

        self._all_connections.clear()
        self._used_connections.clear()
        self._available_connections.clear()

    def _close_connection(self, conn: BOMFTPConn):
        """
        Close an individual connection
        """
        conn.quit()


__all__ = [
    "BOMFTPPool",
]
