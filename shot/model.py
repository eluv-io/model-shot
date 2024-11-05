
import cv2
from typing import List
from loguru import logger

from config import config
from common_ml.tags import VideoTag
from common_ml.model import VideoModel

from .transnet import TransNetV2
from .test_card import TestCardClassifier

class ShotDetector(VideoModel):
    shot_types = ["black", "test card"]

    def __init__(self, transnet_path: str, test_card_dir: str):
        device = config['device']
        self.transnet = TransNetV2(transnet_path, device=device)
        self.test_card_classifier = TestCardClassifier(device, test_card_dir, n_frames=4)

    def tag(self, video_path: str) -> List[VideoTag]:
        logger.debug(f"Running shot detection on {video_path}")
        # get fps
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        cap.release()

        # detect shot transition
        _, shots = self.transnet.predict_shots(video_path)
        shots = shots.cpu().numpy()
        
        frame_dur = (1 / fps) * 1000
        return [VideoTag(
                    start_time=float(shot[0] / fps) * 1000,
                    end_time=float(shot[1] / fps) * 1000 + frame_dur,
                    text="SHOT"
                    ) for shot in shots
                ]
    def track(self) -> str:
        return 'shot'