#!/bin/bash

dirname=$( realpath $(dirname $0)/..)
cd $dirname

# Run database initialization
python3 scripts/init_db.py

python3 run.py