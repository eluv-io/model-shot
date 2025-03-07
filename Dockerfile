FROM continuumio/miniconda3:latest

WORKDIR /elv

RUN apt-get update && apt-get install -y build-essential && apt-get install -y ffmpeg

RUN \
   conda create -n tagenv python=3.8 -y

SHELL ["conda", "run", "-n", "tagenv", "/bin/bash", "-c"]

RUN \
    conda install -y cudatoolkit=10.1 cudnn=7 nccl 

# Create the SSH directory and set correct permissions
RUN mkdir -p /root/.ssh && chmod 700 /root/.ssh

# Add GitHub to known_hosts to bypass host verification
RUN ssh-keyscan -t rsa github.com >> /root/.ssh/known_hosts

ARG SSH_AUTH_SOCK
ENV SSH_AUTH_SOCK ${SSH_AUTH_SOCK}

COPY models ./models

COPY setup.py .
RUN mkdir -p shot

RUN /opt/conda/envs/tagenv/bin/pip install .

COPY shot ./shot
COPY config.yml run.py config.py .

ENTRYPOINT ["/opt/conda/envs/tagenv/bin/python", "run.py"]
