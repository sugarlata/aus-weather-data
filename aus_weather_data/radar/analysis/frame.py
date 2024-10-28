import zlib
import pickle

from .utils import get_intensity_arrays, storm_cell_identification_algorithm


class FrameAnalysis(object):

    def __init__(self, png_data: bytes):
        intensity_arrays = get_intensity_arrays(png_data)
        discrete_cells = storm_cell_identification_algorithm(
            intensity_arrays.intensity_frames[5],  # type: ignore[index]
            intensity_arrays.intensity_labels[7],  # type: ignore[index]
        )

        self.intensity_frames = intensity_arrays.intensity_frames
        self.intensity_labels = intensity_arrays.intensity_labels
        self.intensity_centroids = intensity_arrays.intensity_centroids
        self.discrete_labels = discrete_cells.discrete_labels
        self.discrete_centroids = discrete_cells.discrete_centroids

    def get_serialized_data(self) -> bytes:
        serialized_data = {
            "intensity_frames": zlib.compress(pickle.dumps(self.intensity_frames)),
            "intensity_labels": zlib.compress(pickle.dumps(self.intensity_labels)),
            "intensity_centroids": zlib.compress(
                pickle.dumps(self.intensity_centroids)
            ),
            "discrete_labels": zlib.compress(pickle.dumps(self.discrete_labels)),
            "discrete_centroids": zlib.compress(pickle.dumps(self.discrete_centroids)),
        }
        return pickle.dumps(serialized_data)

    def load_serialized_data(self, serialized_data: bytes):
        data = pickle.loads(serialized_data)
        self.intensity_frames = pickle.loads(zlib.decompress(data["intensity_frames"]))
        self.intensity_labels = pickle.loads(zlib.decompress(data["intensity_labels"]))
        self.intensity_centroids = pickle.loads(
            zlib.decompress(data["intensity_centroids"])
        )
        self.discrete_labels = pickle.loads(
            zlib.decompress(data["discrete_labels"]),
        )
        self.discrete_centroids = pickle.loads(
            zlib.decompress(data["discete_centroids"]),
        )
