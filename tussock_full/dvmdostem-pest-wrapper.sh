#!/bin/bash

WORKING_ROOT="/atlas_scratch/$USER"

$WORKING_ROOT/dvm-dos-tem/dvmdostem -l err --cal-mode -p 100 -m 1000 -s 0 -t 0 -n 0

rm -f simplified-outputs.txt
./pest-helper.py --json-to-obs simplified-outputs.txt --json-location="why-here" 
