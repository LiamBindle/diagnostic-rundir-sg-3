#!/bin/bash

source /home/liam/miniconda3/bin/activate py37
export PYTHONPATH=$PYTHONPATH:/home/liam/sg-restart-regridder
python plot_tracer_over_time.py
