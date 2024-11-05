import os
import shutil
import subprocess

def load_shot():
    res = subprocess.run(['bash', 'pull-models'], stdout=None, stderr=None)
    if res.returncode != 0:
        raise RuntimeError("Failed to pull models")

    print('Cleaning up models directory')
    for model in os.listdir('models'):
        if model != 'shot':
            shutil.rmtree(f'models/{model}')

if not os.path.exists('models/shot'):
    load_shot()