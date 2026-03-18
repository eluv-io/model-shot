import pytest
import os

from config import config
from shot.model import ShotDetector

TEST_FILE = os.path.join(os.path.dirname(__file__), "../test-files/1.mp4")

def test_shot_model():

    model = ShotDetector(config["storage"]["transnet_path"], contiguous=True)
    tags = model.tag(TEST_FILE)
    assert len(tags) > 0
    for tag in tags:
        assert tag.source_media == TEST_FILE
        assert tag.end_time > tag.start_time