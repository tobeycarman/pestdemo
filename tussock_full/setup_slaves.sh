#!/bin/bash

# Helper script for parallel PEST run.

# Tobey Carman
# July 2016

usage () {
  echo "Usage:

    ./setup_slaves.sh [ -h | --help | --cleanup | NSLAVES ]

       -h, --help  Show this message and quit.
       --cleanup   The program will delete all directories and log files matching
                   '$HOME/slv-*' and '$HOME/slv-*.log'
       --start     The program will start a slave in each directory matching '$HOME/slv-*'
       NSLAVES     Program will create N directories starting with '$HOME/slv-00000'
  "
}

list_workers() {
  find $HOME -type d -name "slv-*" 
}

cleanup () {

  find $HOME -type d -name "slv-*" -print0 2>/dev/null| while IFS= read -r -d '' slave_dir
  do
    rm -rf $slave_dir
    echo "Removed '$slave_dir'."
  done

  find $HOME -type f -name "slv-*.log" -print0 2>/dev/null | while IFS= read -r -d '' log_file
  do
    rm $log_file
    echo "Removed '$log_file'."
  done

}

setup_slaves() {

  NSLAVES=$1

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
}

start_slaves() {

  # look for slv-* directories
  find $HOME -type d -name "slv-*" -print0 |  while IFS= read -r -d '' slave_dir
  do
    BN=$(basename "$slave_dir")
    cd "$slave_dir" && pestpp tussock_full.pst/H :5050 > "$HOME/$BN.log" 2>&1 &
    PID=$!
    echo "Started slave with pid=$PID in: '$slave_dir'"
  done
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

  --list )          list_workers
                    exit 0
                    ;;

  --cleanup )       cleanup
                    exit 0
                    ;;

  --start )         start_slaves
                    exit 0
                    ;;

  *)                NSLAVES=$1
                    setup_slaves $NSLAVES
                    ;;
esac

