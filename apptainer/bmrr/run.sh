#!/bin/bash

cd /home/tests/big-mad-robot-repo/$1

if [ "$1" = "qdpy" ]; then
    if [ "$3" = "" ]; then
        python3 ./main.py --seed $2
    else
        python3 ./main.py --seed $2 --objective $3
    fi
elif [ "$1" = "gp" ]; then
    if [ "$3" = "" ]; then
        python3 ./main.py --seed $2
    elif [[ "$4" == "" || "$5" == "" ]]; then
        python3 ./main.py --seed $2 --objective $3
    else
        python3 ./main.py --seed $2 --objective $3 --using_repertoire $4 --bins_per_axis $5
    fi
fi
