import os
from typing import List
from aus_weather_data.radar.analysis.frame_sequence import BOMFrameSequence
from aus_weather_data.radar.remote.download import BOMRadarDownload
from aus_weather_data.radar.common.types import RADAR_TYPE
from aus_weather_data.radar.common.location import BOMRadarLocation
from aus_weather_data.radar.common.frame import BOMRadarFramePNG
from aus_weather_data.radar.analysis.frame import (
    BOMRadarFrameAnalysis,
)


def download_frames():

    with BOMRadarDownload() as bdl:
        bdl.get_radar_frames(
            radar_locations=[BOMRadarLocation.IDR02],
            radar_types=[RADAR_TYPE.REF_128_KM],
            start_time=None,
            end_time=None,
            ignore_list=None,
        )


def load_local_png_frames() -> List[BOMRadarFramePNG]:

    frames: List[BOMRadarFramePNG] = []
    for fn in os.listdir("frames/"):
        if not fn.endswith(".png"):
            continue
        frame = BOMRadarFramePNG(fn)
        frame.load_png_from_file(f"frames/")
        frames.append(frame)

    return frames


def load_local_bra_frames():

    frames: List[BOMRadarFrameAnalysis] = []
    for fn in os.listdir("frames/"):
        if not fn.endswith(".bra"):
            continue

        frame = BOMRadarFrameAnalysis(
            filepath=os.path.join("frames/", fn),
        )
        frames.append(frame)

    return frames


if __name__ == "__main__":
    import time

    # download_frames()
    start_time = time.time()

    # frames = load_local_png_frames()
    # for frame in frames:
    #     frame.save_analysis_data("frames/")

    frames = load_local_bra_frames()
    end_time = time.time()
    # fs = BOMFrameSequence(frames)
    print(f"Completed in {end_time - start_time}")
    breakpoint()
