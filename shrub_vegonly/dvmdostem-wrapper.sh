#!/bin/bash


cd ~/dvm-dos-tem/
./dvmdostem --cal-mode -l note -p 100 -m 100

cd ~/pestdemo/shrub_vegonly/
rm shrub_vegonly-simplified-output.txt
./json2simpletxt.py
