from aus_weather_data.radar.analysis.utils import link_cells
from aus_weather_data.radar.analysis.frame import BOMRadarFrameAnalysis


class BOMFrameSequence(object):

    def __init__(self, frames: list[BOMRadarFrameAnalysis]):
        self._frames = frames
        self._frame_index = {
            frame.frame_id: idx for idx, frame in enumerate(self._frames)
        }

        self.frame_deltas = {
            (self.frame_index(idx - 1), self.frame_index(idx)): link_cells(
                self._frames[idx - 1], self._frames[idx]
            )
            for idx in range(1, len(self._frames))
        }

    def frame_index(self, frame_id: str) -> int:
        return self._frame_index[frame_id]

    def get_frame(self, frame_id: str) -> BOMRadarFrameAnalysis:
        return self._frames[self.frame_index(frame_id)]

    def get_cell_parents(self, frame_filename: str, cell_id: int) -> tuple[str, set]:
        return (
            self._frame_cell_steps[frame_filename]
            .get("parents", {})
            .get("parent_frame", None),
            self._frame_cell_steps[frame_filename]
            .get("parents", {})
            .get(cell_id, set()),
        )

    def get_cell_parents_tree(self, frame_filename: str, cell_id: int) -> dict:
        parent_filename, parent_ids = self.get_cell_parents(frame_filename, cell_id)
        tree = {}
        tree[parent_filename] = {}
        for parent_id in parent_ids:
            tree[parent_filename][parent_id] = self.get_cell_parents_tree(
                parent_filename, parent_id
            )
        return tree

    def get_cell_children(self, frame_filename: str, cell_id: int) -> tuple[str, set]:
        return (
            self._frame_cell_steps[frame_filename]
            .get("children", {})
            .get("child_frame", None),
            self._frame_cell_steps[frame_filename]
            .get("children", {})
            .get(cell_id, set()),
        )

    def get_cell_children_tree(self, frame_filename: str, cell_id: int) -> dict:
        child_filename, child_ids = self.get_cell_children(frame_filename, cell_id)
        tree = {}
        tree[child_filename] = {}
        for child_id in child_ids:
            tree[child_filename][child_id] = self.get_cell_children_tree(
                child_filename, child_id
            )
        return tree

    def get_track(self, frame_filename: str, cell_id: int) -> dict:

        # Get track backwards
        backwards_track = self.get_cell_parents_tree(frame_filename, cell_id)
        forwards_track = self.get_cell_children_tree(frame_filename, cell_id)
        breakpoint()
