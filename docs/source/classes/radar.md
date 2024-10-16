- [Class Diagrams](#class-diagrams)
- [Modules](#modules)
  - [radar](#radar)
    - [download.py](#downloadpy)
      - [BOMRadarDownload](#bomradardownload)
  - [radar.common](#radarcommon)
    - [constants.py](#constantspy)
      - [Credential Constants](#credential-constants)
      - [IDRXX\_DATA](#idrxx_data)
    - [frame\_base.py](#frame_basepy)
      - [BOMRadarFrameBase](#bomradarframebase)
    - [frame\_png.py](#frame_pngpy)
      - [BOMRadarFramePNG](#bomradarframepng)
    - [location.py](#locationpy)
      - [BOMRadarLocation](#bomradarlocation)
    - [types.py](#typespy)
      - [RADAR\_TYPE](#radar_type)
      - [RADAR\_TYPE\_MAP](#radar_type_map)
    - [utils.py](#utilspy)
      - [get\_translation\_coordinate](#get_translation_coordinate)
      - [split\_filename](#split_filename)
  - [radar.common.file\_handling](#radarcommonfile_handling)
    - [base.py](#basepy)
      - [BOMRadarFile](#bomradarfile)
    - [local.py](#localpy)
      - [BOMRadarPNGLocalFile](#bomradarpnglocalfile)
    - [remote.py](#remotepy)
      - [BOMRadarPNGRemoteFile](#bomradarpngremotefile)
  - [radar.remote](#radarremote)
    - [conn.py](#connpy)
      - [BOMFTPConn](#bomftpconn)
    - [pool.py](#poolpy)
      - [BOMFTPPool](#bomftppool)


# Class Diagrams


```mermaid


classDiagram

direction RL
BOMRadarPNGLocalFile <|-- BOMRadarFile
BOMRadarPNGRemoteFile <|-- BOMRadarFile
BOMRadarFramePNG <|-- BOMRadarFrameBase
BOMRadarLocation <|-- Enum
RADAR_TYPE <|-- Enum
BOMRadarDownload <|-- BOMFTPPool

class BOMRadarFile{
    +str filename
    +str path
    +bytes data
}

class BOMRadarPNGLocalFile~BOMRadarFile~{
    +full_path() str
    +load_data_from_file() bytes
    +save_file()
}

class BOMRadarPNGRemoteFile~BOMRadarFile~{
    +full_path() str
}

class BOMRadarFrameBase {
    +pytz.BaseTzInfo tz
    +datetime.datetime start_time
    +datetime.datetime end_time
    ~__init__(str filename, pytz.BaseTzInfo tz)
    ~__str__() str
    ~__repr__() str
    +str radar_id_str
    +BomRadarLocation radar_id
    +str radar_type_str
    +RADAR_TYPE radar_type
    +str radar_id_type_str
    +float epoch_time
    +datetime.datetime dt_utc
    +datetime.datetime dt_locale
    +str year_utc
    +str year_locale
    +str month_utc
    +str month_locale
    +str day_utc
    +str day_locale
    +str hour_utc
    +str hour_locale
    +str minute_utc
    +str minute_locale
    +str date_utc
    +str date_locale
    +str nice_date_utc
    +str nice_date_locale
    +str filename


}

class BOMRadarFramePNG~BOMRadarFrameBase~{
    -str _filename
    -dict _metadata
}

class BOMRadarLocation {
    +holder
}

class RADAR_TYPE {
    +holder
}

class BOMFTPConn {
    +holder
}

class BOMFTPPool {
    +holder
}

class BOMRadarDownload {
    +holder
}

```

# Modules

## radar

### download.py

#### BOMRadarDownload

- Holder

## radar.common

### constants.py

#### Credential Constants

- Holder

#### IDRXX_DATA

- Holder

### frame_base.py

#### BOMRadarFrameBase

- Holder

### frame_png.py

#### BOMRadarFramePNG

- Holder

### location.py

#### BOMRadarLocation

- Holder

### types.py

#### RADAR_TYPE

- Holder

#### RADAR_TYPE_MAP

- Holder

### utils.py

#### get_translation_coordinate

- Holder

#### split_filename

- Holder

## radar.common.file_handling

### base.py

#### BOMRadarFile

- Holder

### local.py

#### BOMRadarPNGLocalFile

- Holder

### remote.py

#### BOMRadarPNGRemoteFile

- Holder

## radar.remote

### conn.py

#### BOMFTPConn

- Holder

### pool.py

#### BOMFTPPool

- Holder
