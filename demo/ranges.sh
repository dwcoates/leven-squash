#!/bin/bash

for C in `seq 100 10 200`
do
    for N in {1..40}
    do
        python run_nc.py -N $N -C $C
    done
done
