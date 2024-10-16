

def test_radar_type_parsing():

    from aus_weather_data.radar.common.types import RADAR_TYPE

    assert RADAR_TYPE("4") == RADAR_TYPE.REF_64_KM
    assert RADAR_TYPE("3") == RADAR_TYPE.REF_128_KM
    assert RADAR_TYPE("2") == RADAR_TYPE.REF_256_KM
    assert RADAR_TYPE("1") == RADAR_TYPE.REF_512_KM
    assert RADAR_TYPE("I") == RADAR_TYPE.VEL_128_KM
    assert RADAR_TYPE("A") == RADAR_TYPE.RAI_128_KM_5M
    assert RADAR_TYPE("B") == RADAR_TYPE.RAI_128_KM_1H
    assert RADAR_TYPE("C") == RADAR_TYPE.RAI_128_KM_9AM
    assert RADAR_TYPE("D") == RADAR_TYPE.RAI_128_KM_24H
    