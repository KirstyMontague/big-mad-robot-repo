#!/bin/bash

mkdir /home/tests/big-mad-robot-repo/argos3/build
cd /home/tests/big-mad-robot-repo/argos3/build

echo "cmake"
cmake -DCMAKE_BUILD_TYPE=Release .. > /dev/null 2>&1

echo "make"
make > /dev/null 2>&1
