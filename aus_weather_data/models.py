import numpy.typing as npt


class IntensityArrays(object):

    def __init__(
        self,
        frame_id: str,
        frames: npt.ArrayLike,
        labels: npt.ArrayLike,
        centroids: npt.ArrayLike,
    ):
        self.frame_id = frame_id
        self.frames = frames
        self.labels = labels
        self.centroids = centroids


class DiscreteCells(object):

    def __init__(
        self,
        frame_id: str,
        labels: npt.ArrayLike,
        centroids: npt.ArrayLike,
    ):
        self.frame_id = frame_id
        self.labels = labels
        self.centroids = centroids


class FrameDelta(object):

    def __init__(
        self,
        previous_frame_id: str,
        next_frame_id: str,
        cell_map_forward: dict,
        cell_map_backward: dict,
        cell_flow: npt.ArrayLike,
    ):
        self.previous_frame_id = previous_frame_id
        self.next_frame_id = next_frame_id
        self.cell_map_forward = cell_map_forward
        self.cell_map_backward = cell_map_backward
        self.cell_flow = cell_flow
