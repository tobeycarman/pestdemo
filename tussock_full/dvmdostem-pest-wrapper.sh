#!/bin/bash

cd ~/dvm-dos-tem
./dvmdostem --cal-mode -p 100 -m 500

cd ~/pestdemo/tussock_full
rm -f simplified-outputs.txt
./pest-helper.py --json-to-obs simplified-outputs.txt

