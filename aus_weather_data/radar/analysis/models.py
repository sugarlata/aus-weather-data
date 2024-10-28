import numpy.typing as npt


class IntensityArrays(object):

    def __init__(
        self,
        intensity_frames: npt.ArrayLike,
        intensity_labels: npt.ArrayLike,
        intensity_centroids: npt.ArrayLike,
    ):
        self.intensity_frames = intensity_frames
        self.intensity_labels = intensity_labels
        self.intensity_centroids = intensity_centroids


class DiscreteCells(object):

    def __init__(
        self,
        discrete_labels: npt.ArrayLike,
        discrete_centroids: npt.ArrayLike,
    ):
        self.discrete_labels = discrete_labels
        self.discrete_centroids = discrete_centroids
