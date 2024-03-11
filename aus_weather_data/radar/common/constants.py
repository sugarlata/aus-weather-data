from aus_weather_data.radar.common.types import RADAR_TYPE


BOM_FTP_HOST = "ftp2.bom.gov.au"
BOM_RADAR_PATH = "/anon/gen/radar"
BOM_FTP_USER = "anonymous"
BOM_FTP_PASS = ""

IDR02_DATA = (
    """
    IDR for Melbourne

    See :class:`aus_weather_data.radar.location.BOMRadarLocation` for inherited methods.

    Attributes:
        radar_types: Contains a list of the radar types that this location supports.
    """,
    "Melbourne",
    -37.86,
    144.76,
    {
        RADAR_TYPE.REF_64_KM,
        RADAR_TYPE.VEL_128_KM,
        RADAR_TYPE.RAI_128_KM_1H,
        RADAR_TYPE.RAI_128_KM_24H,
        RADAR_TYPE.RAI_128_KM_5M,
        RADAR_TYPE.RAI_128_KM_9AM,
    }
)

IDR49_DATA = (
    """
    IDR for Yarrawonga

    See :class:`aus_weather_data.radar.location.BOMRadarLocationBase` for inherited methods.

    Attributes:
        radar_types: Contains a list of the radar types that this location supports.
    """,
    "Yarrawonga",
    -36.03,
    146.03,
    {
        RADAR_TYPE.REF_64_KM,
        RADAR_TYPE.VEL_128_KM,
    }
)

IDR68_DATA = (
    """
        IDR for Bairnsdale

        See :class:`aus_weather_data.radar.location.BOMRadarLocationBase` for inherited methods.

        Attributes:
            radar_types: Contains a list of the radar types that this location supports.
        """,
    "Bairnsdale",
    -37.89,
    147.56,
    {
        RADAR_TYPE.VEL_128_KM,
    }
)

IDR95_DATA = (
    """
    IDR for Rainbow

    See :class:`aus_weather_data.radar.location.BOMRadarLocationBase` for inherited methods.

    Attributes:
        radar_types: Contains a list of the radar types that this location supports.
    """,
    "Rainbow",
    -35.99,
    142.01,
    {
        RADAR_TYPE.REF_64_KM,
        RADAR_TYPE.VEL_128_KM,
        RADAR_TYPE.RAI_128_KM_1H,
        RADAR_TYPE.RAI_128_KM_24H,
        RADAR_TYPE.RAI_128_KM_5M,
        RADAR_TYPE.RAI_128_KM_9AM,
    }
)

IDR97_DATA = (
    """
    IDR for Mildura

    See :class:`aus_weather_data.radar.location.BOMRadarLocationBase` for inherited methods.

    Attributes:
        radar_types: Contains a list of the radar types that this location supports.
    """,

    "Mildura",
    -34.28,
    141.59,
    {

        RADAR_TYPE.REF_64_KM,
        RADAR_TYPE.VEL_128_KM,
        RADAR_TYPE.RAI_128_KM_1H,
        RADAR_TYPE.RAI_128_KM_24H,
        RADAR_TYPE.RAI_128_KM_5M,
        RADAR_TYPE.RAI_128_KM_9AM,
    }
)

IDR55_DATA = (
    """
    IDR for Wagga Wagga

    See :class:`aus_weather_data.radar.location.BOMRadarLocationBase` for inherited methods.

    Attributes:
        radar_types: Contains a list of the radar types that this location supports.
    """,

    "Wagga Wagga",
    -35.17,
    147.47,
    {}
)

IDR71_DATA = (
    """
        IDR for Sydney

        See :class:`aus_weather_data.radar.location.BOMRadarLocationBase` for inherited methods.

        Attributes:
            radar_types: Contains a list of the radar types that this location supports.
        """,

    "Sydney",
    -33.701,
    151.21,
    {

        RADAR_TYPE.REF_64_KM,
        RADAR_TYPE.VEL_128_KM,
        RADAR_TYPE.RAI_128_KM_1H,
        RADAR_TYPE.RAI_128_KM_24H,
        RADAR_TYPE.RAI_128_KM_5M,
        RADAR_TYPE.RAI_128_KM_9AM,
    }
)

IDR03_DATA = (
    """
        IDR for Wollongong

        See :class:`aus_weather_data.radar.location.BOMRadarLocationBase` for inherited methods.

        Attributes:
            radar_types: Contains a list of the radar types that this location supports.
        """,

    "Wollongong",
    -34.264,
    150.874,
    {

        RADAR_TYPE.REF_64_KM,
        RADAR_TYPE.VEL_128_KM,
        RADAR_TYPE.RAI_128_KM_1H,
        RADAR_TYPE.RAI_128_KM_24H,
        RADAR_TYPE.RAI_128_KM_5M,
        RADAR_TYPE.RAI_128_KM_9AM,
    }
)

IDR96_DATA = (
    """
        IDR for Yeoval

        See :class:`aus_weather_data.radar.location.BOMRadarLocationBase` for inherited methods.

        Attributes:
            radar_types: Contains a list of the radar types that this location supports.
        """,

    "Yeoval",
    -32.74,
    148.7,
    {

        RADAR_TYPE.REF_64_KM,
        RADAR_TYPE.VEL_128_KM,
        RADAR_TYPE.RAI_128_KM_1H,
        RADAR_TYPE.RAI_128_KM_24H,
        RADAR_TYPE.RAI_128_KM_5M,
        RADAR_TYPE.RAI_128_KM_9AM,
    }
)

IDR40_DATA = (
    """
        IDR for Canberra

        See :class:`aus_weather_data.radar.location.BOMRadarLocationBase` for inherited methods.

        Attributes:
            radar_types: Contains a list of the radar types that this location supports.
        """,

    "Canberra",
    -35.66,
    149.51,
    {

        RADAR_TYPE.REF_64_KM,
        RADAR_TYPE.VEL_128_KM,
        RADAR_TYPE.RAI_128_KM_1H,
        RADAR_TYPE.RAI_128_KM_24H,
        RADAR_TYPE.RAI_128_KM_5M,
        RADAR_TYPE.RAI_128_KM_9AM,
    }
)

IDR94_DATA = (
    """
        IDR for Hillston

        See :class:`aus_weather_data.radar.location.BOMRadarLocationBase` for inherited methods.

        Attributes:
            radar_types: Contains a list of the radar types that this location supports.
        """,

    "Hillston",
    -33.55,
    145.52,
    {

        RADAR_TYPE.REF_64_KM,
        RADAR_TYPE.VEL_128_KM,
        RADAR_TYPE.RAI_128_KM_1H,
        RADAR_TYPE.RAI_128_KM_24H,
        RADAR_TYPE.RAI_128_KM_5M,
        RADAR_TYPE.RAI_128_KM_9AM,
    }
)

IDR64_DATA = (
    """
        IDR for Adelaide (Buckland Park)

        See :class:`aus_weather_data.radar.location.BOMRadarLocationBase` for inherited methods.

        Attributes:
            radar_types: Contains a list of the radar types that this location supports.
        """,

    "Adelaide (Buckland Park)",
    -34.617,
    138.469,
    {

        RADAR_TYPE.REF_64_KM,
        RADAR_TYPE.VEL_128_KM,
        RADAR_TYPE.RAI_128_KM_1H,
        RADAR_TYPE.RAI_128_KM_24H,
        RADAR_TYPE.RAI_128_KM_5M,
        RADAR_TYPE.RAI_128_KM_9AM,
    }
)

IDR46_DATA = (
    """
        IDR for Adelaide (Sellicks Hill)

        See :class:`aus_weather_data.radar.location.BOMRadarLocationBase` for inherited methods.

        Attributes:
            radar_types: Contains a list of the radar types that this location supports.
        """,

    "Adelaide (Sellicks Hill)",
    -35.33,
    138.5,
    {

        RADAR_TYPE.RAI_128_KM_1H,
        RADAR_TYPE.RAI_128_KM_24H,
        RADAR_TYPE.RAI_128_KM_5M,
        RADAR_TYPE.RAI_128_KM_9AM,
    }
)

IDR33_DATA = (
    """
        IDR for Ceduna

        See :class:`aus_weather_data.radar.location.BOMRadarLocationBase` for inherited methods.

        Attributes:
            radar_types: Contains a list of the radar types that this location supports.
        """,

    "Ceduna",
    -32.13,
    133.7,
    {

        RADAR_TYPE.REF_64_KM,
        RADAR_TYPE.VEL_128_KM,
        RADAR_TYPE.RAI_128_KM_1H,
        RADAR_TYPE.RAI_128_KM_24H,
        RADAR_TYPE.RAI_128_KM_5M,
        RADAR_TYPE.RAI_128_KM_9AM,
    }
)
