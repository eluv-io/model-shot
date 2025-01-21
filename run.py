import argparse
from typing import List
import os
import json
from dataclasses import asdict, dataclass
from common_ml.types import Data

from shot.model import ShotDetector
from config import config


# shot detection takes no config params
@dataclass
class RuntimeConfig(Data):
    pass

    @staticmethod
    def from_dict(data: dict) -> 'RuntimeConfig':
        return RuntimeConfig()

def run(video_paths: List[str], runtime_config: str=None) -> None:
    shot_detector = ShotDetector(config["storage"]["transnet_path"], config["storage"]["test_card_path"])
    tags_out = os.getenv('TAGS_PATH', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tags'))
    if not os.path.exists(tags_out):
        os.makedirs(tags_out)
    for fname in video_paths:
        tags = shot_detector.tag(fname)
        if len(tags) == 0:
            continue
        out_fname = os.path.join(tags_out, f"{os.path.basename(fname)}_tags.json")
        with open(out_fname, 'w') as f:
            f.write(json.dumps([asdict(tag) for tag in tags]))
            
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('video_paths', nargs='+', type=str)
    parser.add_argument('--config', type=str, default=None)
    args = parser.parse_args()
    run(args.video_paths, args.config)