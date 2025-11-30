#!/bin/bash

mkdir /home/tests/argos3/build_simulator
cd /home/tests/argos3/build_simulator

echo "cmake ../src"
cmake -DCMAKE_BUILD_TYPE=Release ../src > /dev/null 2>&1

echo "make doc"
make doc > /dev/null 2>&1

echo "make install"
make install > /dev/null 2>&1
