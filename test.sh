#!/bin/bash

[ "$ELV_MODEL_TEST_GPU_TO_USE" != "" ] || ELV_MODEL_TEST_GPU_TO_USE=0

set -x

mkdir .cache-ro

rm -rf test_output/
mkdir -p test_output/{gpu,cpu}

time podman run --rm  --volume=$(pwd)/test:/elv/test:ro --volume=$(pwd)/.cache-ro:/root/.cache:ro --volume=$(pwd)/test_output/cpu:/elv/tags --network host shot test/1.mp4 test/2.mp4

ex1=$?

time podman run --rm  --volume=$(pwd)/test:/elv/test:ro --volume=$(pwd)/.cache-ro:/root/.cache:ro --volume=$(pwd)/test_output/gpu:/elv/tags --network host --device nvidia.com/gpu=$ELV_MODEL_TEST_GPU_TO_USE shot test/1.mp4 test/2.mp4

ex=$?

cd test_output
find

if [ "$ex1" != "0" ]; then
    exit $ex1
fi

exit $ex
