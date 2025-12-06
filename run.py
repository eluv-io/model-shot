import argparse
from typing import List, Callable
import os
import json
from dataclasses import asdict, dataclass
import setproctitle
from dacite import from_dict

from common_ml.model import run_live_mode
from common_ml.utils import nested_update

from shot.model import ShotDetector
from config import config

@dataclass
class RuntimeConfig:
    contiguous: bool

def make_tag_fn(cfg: RuntimeConfig) -> Callable:

    model = ShotDetector(config["storage"]["transnet_path"], contiguous=cfg.contiguous)
    tags_out = os.getenv('TAGS_PATH', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tags'))
    if not os.path.exists(tags_out):
        os.makedirs(tags_out)

    def tag_fn(video_paths: List[str]) -> None:
        for fname in video_paths:
            tags = model.tag(fname)
            if len(tags) == 0:
                continue
            out_fname = os.path.join(tags_out, f"{os.path.basename(fname)}_tags.json")
            with open(out_fname, 'w') as f:
                f.write(json.dumps([asdict(tag) for tag in tags]))

    return tag_fn

if __name__ == '__main__':
    setproctitle.setproctitle('model-shot')    
    parser = argparse.ArgumentParser()
    parser.add_argument('video_paths', nargs='*', type=str, default=[])
    parser.add_argument('--config', type=str, default=None)
    parser.add_argument('--live', action='store_true', default=False)
    args = parser.parse_args()
    
    cfg_raw = json.loads(args.config) if args.config else {}
    default_cfg = config["runtime"]["default"]

    runtime_cfg = from_dict(data_class=RuntimeConfig, data=nested_update(default_cfg, cfg_raw))
    tag_fn = make_tag_fn(runtime_cfg)

    if args.live:
        print('Running in live mode...')
        run_live_mode(tag_fn)
    else:
        tag_fn(args.video_paths)