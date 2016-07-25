#!/bin/bash

# idea for script to setup a slave for a PEST Run...

# assumptions:
#  - you have a copy of the dvmdostem repo in your home directory
#  - you have a copy of the pestdemo repo in your home directory

#  - this script may create (and eventually delete?) N subdirecrories in
#    your ~/ folder, one for each slave


# 1) make x subdirectorys
mkdir -p ~/s1
mkdir -p ~/s2
mkdir -p ~/s3
mkdir -p ~/s4
mkdir -p ~/s5
mkdir -p ~/s6


# 2) copy config, params from ~/dvmdostem/ to each slave directory
mkdir -p ~/s1/config && cp -r ~/dvm-dos-tem/config ~/s1/
mkdir -p ~/s2/config && cp -r ~/dvm-dos-tem/config ~/s2/
mkdir -p ~/s3/config && cp -r ~/dvm-dos-tem/config ~/s3/
mkdir -p ~/s4/config && cp -r ~/dvm-dos-tem/config ~/s4/
mkdir -p ~/s5/config && cp -r ~/dvm-dos-tem/config ~/s5/
mkdir -p ~/s6/config && cp -r ~/dvm-dos-tem/config ~/s6/


mkdir -p ~/s1/parameters && cp -r ~/dvm-dos-tem/parameters ~/s1/
mkdir -p ~/s2/parameters && cp -r ~/dvm-dos-tem/parameters ~/s2/
mkdir -p ~/s3/parameters && cp -r ~/dvm-dos-tem/parameters ~/s3/
mkdir -p ~/s4/parameters && cp -r ~/dvm-dos-tem/parameters ~/s4/
mkdir -p ~/s5/parameters && cp -r ~/dvm-dos-tem/parameters ~/s5/
mkdir -p ~/s6/parameters && cp -r ~/dvm-dos-tem/parameters ~/s6/

mkdir -p ~/s1/output
mkdir -p ~/s2/output
mkdir -p ~/s3/output
mkdir -p ~/s4/output
mkdir -p ~/s5/output
mkdir -p ~/s6/output

touch ~/s1/output/restart-eq.nc
touch ~/s2/output/restart-eq.nc
touch ~/s3/output/restart-eq.nc
touch ~/s4/output/restart-eq.nc
touch ~/s5/output/restart-eq.nc
touch ~/s6/output/restart-eq.nc

# 4) modify the config file:
  # - By clever workings, it looks like it si poosible to generalize this enough to
  # do it onece and then copy to all the ~/sN directories...

cp ~/pestdemo/tussock_full/tussock_full.pst ~/s1/
cp ~/pestdemo/tussock_full/tussock_full.pst ~/s2/
cp ~/pestdemo/tussock_full/tussock_full.pst ~/s3/
cp ~/pestdemo/tussock_full/tussock_full.pst ~/s4/
cp ~/pestdemo/tussock_full/tussock_full.pst ~/s5/
cp ~/pestdemo/tussock_full/tussock_full.pst ~/s6/

# copy the pest controlfile, template, wrapper, and helper 
# from ~/pestdemo to each slave directory
cp ~/pestdemo/tussock_full/cmt_calparbgc.tpl ~/s1
cp ~/pestdemo/tussock_full/cmt_calparbgc.tpl ~/s2
cp ~/pestdemo/tussock_full/cmt_calparbgc.tpl ~/s3
cp ~/pestdemo/tussock_full/cmt_calparbgc.tpl ~/s4
cp ~/pestdemo/tussock_full/cmt_calparbgc.tpl ~/s5
cp ~/pestdemo/tussock_full/cmt_calparbgc.tpl ~/s6

cp ~/pestdemo/tussock_full/dvmdostem-pest-wrapper.sh ~/s1
cp ~/pestdemo/tussock_full/dvmdostem-pest-wrapper.sh ~/s2
cp ~/pestdemo/tussock_full/dvmdostem-pest-wrapper.sh ~/s3
cp ~/pestdemo/tussock_full/dvmdostem-pest-wrapper.sh ~/s4
cp ~/pestdemo/tussock_full/dvmdostem-pest-wrapper.sh ~/s5
cp ~/pestdemo/tussock_full/dvmdostem-pest-wrapper.sh ~/s6

cp ~/pestdemo/tussock_full/read-simple-outputs.ins ~/s1
cp ~/pestdemo/tussock_full/read-simple-outputs.ins ~/s2
cp ~/pestdemo/tussock_full/read-simple-outputs.ins ~/s3
cp ~/pestdemo/tussock_full/read-simple-outputs.ins ~/s4
cp ~/pestdemo/tussock_full/read-simple-outputs.ins ~/s5
cp ~/pestdemo/tussock_full/read-simple-outputs.ins ~/s6

cp ~/pestdemo/tussock_full/pest-helper.py ~/s1
cp ~/pestdemo/tussock_full/pest-helper.py ~/s2
cp ~/pestdemo/tussock_full/pest-helper.py ~/s3
cp ~/pestdemo/tussock_full/pest-helper.py ~/s4
cp ~/pestdemo/tussock_full/pest-helper.py ~/s5
cp ~/pestdemo/tussock_full/pest-helper.py ~/s6



