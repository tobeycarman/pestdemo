#!/bin/bash

cd ~/dvm-dos-tem
./dvmdostem --cal-mode -l note -p 10 -m 25

cd ~/pestdemo/tussock_full
rm -f simplified-outputs.txt
./pest-helper.py --json2obs simplified-outputs.txt

