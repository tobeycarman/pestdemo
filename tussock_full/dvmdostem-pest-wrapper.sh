#!/bin/bash

# cd ~/dvm-dos-tem
# 
# cat << EOF > "config/calibration_directives.txt"
# // calibration directives, autogenerated by dvmdostem-pest-wrapper.sh for PEST run.
# {
#   "calibration_autorun_settings": {
#     "0": ["dsl on", "nfeed on", "dsb off"],
#     "pwup": false // "post warm up pause", [true | false], boolean
#   }
# }
# EOF
# 
# PID_TAG="auto123"

$HOME/dvm-dos-tem/dvmdostem -l fatal --cal-mode -p 100 -m 1000

rm -f simplified-outputs.txt
./pest-helper.py --json-to-obs simplified-outputs.txt --json-location="why-here" 
