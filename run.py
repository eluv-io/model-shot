import argparse
import os
import json
from dataclasses import dataclass
import setproctitle
from dacite import from_dict

from common_ml.tagging.run_helpers import start_loop_from_av_model

from shot.model import ShotDetector
from config import config

@dataclass
class RuntimeConfig:
    # if contiguous is False, then we tag each input file independently, 
    # otherwise we assume input files are contiguous segments of a larger video and we allow shots to span across input files. 
    contiguous: bool = True

def _parse_config_string(config_str: str) -> RuntimeConfig:
    config_dict = json.loads(config_str)
    return from_dict(RuntimeConfig, config_dict)

if __name__ == '__main__':
    setproctitle.setproctitle('model-shot')    
    parser = argparse.ArgumentParser()
    parser.add_argument('--output-path', type=str, required=True, help='Path to save the output tags')
    parser.add_argument('--params', type=str, default=None, help='JSON string of parameters to override the default config')
    args = parser.parse_args()
    
    params = _parse_config_string(args.params) if args.params else RuntimeConfig()

    model = ShotDetector(config["storage"]["transnet_path"], contiguous=params.contiguous)

    start_loop_from_av_model(model, args.output_path)