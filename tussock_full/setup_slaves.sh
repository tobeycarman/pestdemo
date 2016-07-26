#!/bin/bash

# Helper script for parallel PEST run.

# Tobey Carman
# July 2016

function usage () {
  echo "Usage:
  
    ./setup_slaves.sh [ -h | --help | --cleanup | NSLAVES ]

       -h, --help  Show this message and quit.
       --cleanup   The program will delete all directories matching $HOME/slv-*
       NSLAVES     Program will create directories matching $HOME/slv-00000
  "
}

function cleanup () {
  
  find $HOME -type d -name "slv-*" 2>/dev/null | xargs rm -rf

#   DIRLIST=$( find $HOME -type d -name "slv-*" 2>/dev/null )
#   echo "Forcibly removing these directories:"
#   for i in "${DIRLIST[@]}"
#   do
#     echo "$i"
#     rm -rf "$i"
#   done  
}

NSLAVES=

# Check that user supplied exactly one argument
if [[ "$#" -ne 1 ]]
then
  usage
  exit -1
fi

case $1 in

  -h | --help )     usage
                    exit 0
                    ;;

  --cleanup )       cleanup
                    exit 0
                    ;;

  *)                NSLAVES=$1
                    ;;
esac

# Check that the argument supplied can be converted to an integer...
python -c "int($NSLAVES)" > /dev/null 2>&1
if [[ $? -ne 0 ]]
then
  usage
  echo "ERROR: '$NSLAVES' cannot be converted to an integer!"
  exit -1
fi

echo "Will try creating directory structure for $NSLAVES..."
if [[ $NSLAVES -gt 25 ]]
then
  echo "I refuse. Thats too many directories to create!"
  exit -1
fi

for (( i=0; i <= $NSLAVES; ++i ))
do
  printf -v ZPNUM "%05d" $i # Zero padded number
  FULL_SPATH="$HOME/slv-$ZPNUM"

  mkdir -p $FULL_SPATH
  mkdir -p $FULL_SPATH/config && cp -r ~/dvm-dos-tem/config $FULL_SPATH/
  mkdir -p $FULL_SPATH/parameters && cp -r ~/dvm-dos-tem/parameters $FULL_SPATH/
  mkdir -p $FULL_SPATH/output
  touch $FULL_SPATH/output/restart-eq.nc
  cp ~/pestdemo/tussock_full/tussock_full.pst $FULL_SPATH
  cp ~/pestdemo/tussock_full/cmt_calparbgc.tpl $FULL_SPATH
  cp ~/pestdemo/tussock_full/dvmdostem-pest-wrapper.sh $FULL_SPATH
  cp ~/pestdemo/tussock_full/read-simple-outputs.ins $FULL_SPATH
  cp ~/pestdemo/tussock_full/pest-helper.py $FULL_SPATH

done

