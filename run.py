
import json
from dataclasses import dataclass
import setproctitle
from dacite import from_dict

from common_ml.tagging.run_helpers import run_default, catch_errors, get_params

from shot.model import ShotDetector
from config import config

@dataclass
class RuntimeConfig:
    # if contiguous is False, then we tag each input file independently, 
    # otherwise we assume input files are contiguous segments of a larger video and we allow shots to span across input files. 
    contiguous: bool = True

if __name__ == '__main__':
    setproctitle.setproctitle('model-shot')
    
    catch_errors()
    params = get_params()
    params = from_dict(RuntimeConfig, params)

    model = ShotDetector(config["storage"]["transnet_path"], contiguous=params.contiguous)

    run_default(model)