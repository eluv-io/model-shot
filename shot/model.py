
import cv2
from typing import List
from loguru import logger

from common_ml.tags import VideoTag
from common_ml.model import VideoModel

from .transnet import TransNetV2

import torch

class ShotDetector(VideoModel):
    shot_types = ["black", "test card"]

    def __init__(
        self, 
        transnet_path: str,
        contiguous: bool
    ):
        if torch.cuda.is_available():
            logger.info("cuda is available, using it")
            device = "cuda"
        else:
            logger.warning("cuda not available, using cpu (still faster than realtime)")
            device = "cpu"

        self.transnet = TransNetV2(transnet_path, device=device)

        self.last_fps = None
        self.abs_curr_start = 0
        self.abs_next_start = 0
        self.contiguous = contiguous

    def tag(self, fpath: str) -> List[VideoTag]:
        logger.debug(f"Running shot detection on {fpath}")

        # get fps
        cap = cv2.VideoCapture(fpath)
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration_ms = (frame_count / fps) * 1000
        frame_time = 1000 / fps
        cap.release()

        if fps != self.last_fps and self.last_fps is not None:
            logger.warning(f"Video fps changed from {self.last_fps} to {fps}")
            self.last_fps = fps

        transition_idx = self.transnet.predict_shots(fpath)

        res = []

        for idx in transition_idx:
            relative_end_ts = (idx / fps) * 1000
            # might be from an earlier segment
            relative_start_ts = self.abs_next_start - self.abs_curr_start

            start_time = int(relative_start_ts)+frame_time
            end_time = int(relative_end_ts)

            if start_time >= end_time:
                # happens with black frames at the beginning
                continue

            res.append(VideoTag(
                text="",
                start_time=int(relative_start_ts+frame_time),
                end_time=int(relative_end_ts),
            ))

            self.abs_next_start = relative_end_ts + self.abs_curr_start

        if self.contiguous:
            self.abs_curr_start += duration_ms
        else:
            self.abs_next_start = 0
            self.abs_curr_start = 0

        return res