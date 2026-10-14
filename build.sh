#!/bin/bash

set -e

SCRIPT_PATH="$(dirname "$(realpath "$0")")"
MODEL_PATH=$(yq -r .storage.model_path $SCRIPT_PATH/config.yml)

mkdir -p models
rsync --progress --update --times --recursive --links --delete $MODEL_PATH/ $SCRIPT_PATH/models/shot/

exec buildscripts/build_container.bash -t "shot:${IMAGE_TAG:-latest}" . -f Containerfile