#!/bin/bash

dirname=$( realpath $(dirname $0)/..)
cd $dirname

source .venv/bin/activate
python3 run.py