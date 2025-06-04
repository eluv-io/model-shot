from setuptools import setup

setup(
        name="shot",
        version="0.1",
        packages=["shot"],
        install_requires=[
            'opencv-python==4.2.0.34',
            'torch==1.9.0',
            'torchvision==0.10.0',
            'Pillow==9.4.0',
            'scikit-learn',
            'wget',
            'ffmpeg-python==0.2.0',
            'docopt',
            'schema',
            'psutil',
            'loguru==0.5.2',
            'tqdm',
            'nltk',
            'jiwer',
            'argparse==1.4.0',
            'facenet_pytorch==2.5.2',
            'ujson',
            'mxnet-cu101==1.8.0',
            'common_ml @ git+ssh://git@github.com/eluv-io/common-ml.git#egg=common_ml',
            'quick_test_py @ git+https://github.com/eluv-io/quick_test_py.git#egg=quick_test_py'
        ]
)