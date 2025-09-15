import png  # type: ignore[import-untyped]
import numpy as np
import numpy.typing as npt

from skimage import morphology  # type: ignore[import-untyped]
from scipy import ndimage as ndi  # type: ignore[import-untyped]
from skimage.segmentation import watershed  # type: ignore[import-untyped]


from aus_weather_data.models import IntensityArrays, DiscreteCells


def get_intensity_arrays(
    frame_id: str,
    png_data: bytes,
    cell_size_threshold: int = 35,
) -> IntensityArrays:

    color_intensity_map = {
        "(245, 245, 255, 255)": 1,
        "(180, 180, 255, 255)": 2,
        "(120, 120, 255, 255)": 3,
        "(20, 20, 255, 255)": 4,
        "(0, 216, 195, 255)": 5,
        "(0, 150, 144, 255)": 6,
        "(0, 102, 102, 255)": 7,
        "(255, 255, 0, 255)": 8,
        "(255, 200, 0, 255)": 9,
        "(255, 150, 0, 255)": 10,
        "(255, 100, 0, 255)": 11,
        "(255, 0, 0, 255)": 12,
        "(200, 0, 0, 255)": 13,
        "(120, 0, 0, 255)": 14,
        "(40, 0, 0, 255)": 15,
    }

    # Open the file with the PNG reader:
    reader = png.Reader(bytes=png_data)
    png_frame = reader.read()

    palette_map = {
        k: color_intensity_map.get(str(v), 0)
        for k, v in enumerate(png_frame[3]["palette"])
    }

    keys = np.array(list(palette_map.keys()))
    values = np.array(list(palette_map.values()), dtype=np.uint8)

    mapping_array = np.zeros(keys.max() + 1, dtype=values.dtype)
    mapping_array[keys] = values

    frame_array = mapping_array[list(png_frame[2])]
    frame_array.shape = (png_frame[3]["size"][0], png_frame[3]["size"][1])

    intensity_frame_list = [
        np.where(frame_array >= intensity, intensity, 0) for intensity in range(1, 16)
    ]

    # Insert Array of zeros at the beginning of the list, makes the indexing easier
    intensity_frame_list.insert(0, np.zeros_like(frame_array))

    frame_labels_list = [
        ndi.label(
            morphology.remove_small_holes(
                morphology.remove_small_objects(
                    intensity_frame.astype(bool),
                    min_size=cell_size_threshold,
                    connectivity=1,
                ),
                cell_size_threshold,
                1,
            ),
            structure=np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]]),
        )[0]
        for intensity_frame in intensity_frame_list
    ]

    frame_intensity_list = [
        np.where(frame != 0, intensity, 0)
        for intensity, frame in enumerate(frame_labels_list)
    ]

    centroids = [
        np.array(
            ndi.center_of_mass(
                frame,
                labels=frame_labels_list[idx],
                index=range(1, frame_labels_list[idx].max() + 1),
            )
        )
        for idx, frame in enumerate(frame_intensity_list)
    ]

    return IntensityArrays(
        frame_id,
        np.array(frame_intensity_list, dtype=np.uint8),
        np.array(frame_labels_list, dtype=np.uint16),
        centroids,
    )


def get_discrete_cells(
    frame_id: str,
    intensity_frames: npt.ArrayLike,
    intensity_labels: npt.ArrayLike,
) -> DiscreteCells:
    distance = ndi.distance_transform_edt(intensity_frames)

    discrete_labels = watershed(
        -distance,
        intensity_labels,
        mask=intensity_frames.astype(bool),  # type: ignore[union-attr]
    )

    discrete_centroids = np.array(
        ndi.center_of_mass(
            discrete_labels,
            labels=intensity_labels,
            index=range(1, intensity_labels.max() + 1),  # type: ignore[union-attr]
        )
    )

    return DiscreteCells(frame_id, discrete_labels, discrete_centroids)
