#!/bin/bash

cd ~/dvm-dos-tem
./dvmdostem --cal-mode -l note -p 10 -m 25

cd ~/pestdemo/
rm -f shrub_vegonly/simplified-output.csv
./json2simpletxt.py shrub_vegonly/simplified-output.csv
