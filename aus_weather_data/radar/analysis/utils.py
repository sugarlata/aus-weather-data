import cv2
import numpy as np

from scipy import ndimage as ndi  # type: ignore[import-untyped]

from aus_weather_data.models import DiscreteCells, FrameDelta


def link_cells(
    discrete_cells_1: DiscreteCells, discrete_cells_2: DiscreteCells
) -> FrameDelta:

    optical_flow_field = cv2.calcOpticalFlowFarneback(
        np.where(discrete_cells_1.labels, 255, 0),
        np.where(discrete_cells_2.labels, 255, 0),
        None,
        0.5,
        3,
        15,
        3,
        5,
        1.2,
        0,
    )

    binary_mask = np.where(discrete_cells_1.labels, 1, 0)

    h, w = binary_mask.shape
    y, x = np.meshgrid(np.arange(h), np.arange(w), indexing="ij")

    flow_x, flow_y = -optical_flow_field[:, :, 0], -optical_flow_field[:, :, 1]

    new_x = np.clip(x + flow_x, 0, w - 1).astype(int)
    new_y = np.clip(y + flow_y, 0, h - 1).astype(int)

    translated_label_matrix = ndi.map_coordinates(
        discrete_cells_1.labels, [new_y.ravel(), new_x.ravel()], order=1, mode="nearest"
    )
    translated_label_matrix = translated_label_matrix.reshape(
        discrete_cells_1.labels.shape
    )

    translated_binary_matrix = np.where(
        translated_label_matrix[translated_label_matrix >= 0], 1, 0
    ).reshape(translated_label_matrix.shape)
    frame_2_binary_matrix = np.where(discrete_cells_2.labels, 1, 0)

    intersection_binary_matrix = translated_binary_matrix * frame_2_binary_matrix
    intersection_label_matrix = ndi.label(intersection_binary_matrix)[0]

    frame_1_children = {}
    frame_2_parents = {}
    for intersection_label_idx in range(1, intersection_label_matrix.max() + 1):
        binary_intersection_sub_matrix = np.where(
            intersection_label_matrix == intersection_label_idx, 1, 0
        )
        frame_1_intersection_values, frame_1_intersection_count = np.unique(
            translated_label_matrix * binary_intersection_sub_matrix,
            return_counts=True,
        )
        frame_1_overlaps = [
            x
            for x in zip(frame_1_intersection_values, frame_1_intersection_count)
            if x[1] > 0
        ]

        frame_2_intersection_values, frame_2_intersection_count = np.unique(
            discrete_cells_2.labels * binary_intersection_sub_matrix,
            return_counts=True,
        )
        frame_2_overlaps = [
            x
            for x in zip(frame_2_intersection_values, frame_2_intersection_count)
            if x[1] > 0
        ]

        intersection = binary_intersection_sub_matrix.sum()

        frame_1_overlap_ratios = [
            x[0] for x in frame_1_overlaps if 1.7 > x[1] / intersection > 0.6
        ]

        frame_2_overlap_ratios = [
            x[0] for x in frame_2_overlaps if 1.7 > x[1] / intersection > 0.6
        ]

        for frame_2_label in frame_2_overlap_ratios:
            frame_2_parents.setdefault(int(frame_2_label), set())
            for frame_1_label_id in frame_1_overlap_ratios:
                frame_2_parents[int(frame_2_label)].add(int(frame_1_label_id))

        for frame_1_label in frame_1_overlap_ratios:
            frame_1_children.setdefault(int(frame_1_label), set())
            for frame_2_label_id in frame_2_overlap_ratios:
                frame_1_children[int(frame_1_label)].add(int(frame_2_label_id))

    frame_2_parents["parent_frame"] = discrete_cells_1.frame_id
    frame_1_children["child_frame"] = discrete_cells_2.frame_id

    return FrameDelta(
        previous_frame_filename=discrete_cells_1.frame_id,
        next_frame_filename=discrete_cells_2.frame_id,
        cell_map_forward=frame_1_children,
        cell_map_backward=frame_2_parents,
        cell_flow=optical_flow_field,
    )
