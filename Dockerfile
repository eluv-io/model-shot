FROM continuumio/miniconda3:latest

WORKDIR /elv

RUN apt-get update && apt-get install -y build-essential && apt-get install -y ffmpeg

RUN \
   conda create -n shot python=3.7.16 -y

SHELL ["conda", "run", "-n", "shot", "/bin/bash", "-c"]

RUN \
    conda install -y cudatoolkit=10.1 cudnn=7 nccl 

COPY shot ./shot
COPY config.yml run.py setup.py config.py .

RUN /opt/conda/envs/shot/bin/pip install .

COPY models ./models

ENTRYPOINT ["/opt/conda/envs/shot/bin/python", "run.py"]