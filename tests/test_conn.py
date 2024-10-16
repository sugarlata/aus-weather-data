from .constants import TEST_WITH_CONNECTION


def test_single_connection():

    if not TEST_WITH_CONNECTION:
        return

    from aus_weather_data.radar.remote.conn import BOMFTPConn
    from aus_weather_data.constants import BOM_RADAR_PATH

    with BOMFTPConn() as conn:

        directory_contents = conn.get_directory_contents(BOM_RADAR_PATH)

    assert directory_contents is not None
    assert type(directory_contents) is list
