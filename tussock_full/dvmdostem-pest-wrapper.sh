#!/bin/bash

/atlas_scratch/$USER/dvm-dos-tem/dvmdostem -l fatal --cal-mode -p 100 -m 1000

rm -f simplified-outputs.txt
./pest-helper.py --json-to-obs simplified-outputs.txt --json-location="why-here" 
