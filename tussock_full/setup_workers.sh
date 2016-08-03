#!/bin/bash

# Helper script for parallel PEST run.

# Tobey Carman
# July 2016

usage () {
  echo "Usage:

    ./setup_workers.sh [ -h | --help | --cleanup | NWORKERS ]

       -h, --help  Show this message and quit.
       --list      Show info about any existing worker directories
       --cleanup   The program will delete all directories and log files matching
                   '$HOME/wrkr-*', '$HOME/master-*' and '$HOME/wrkr-*.log' and '$HOME/master-*.log'
       --start     The program will start a worker in each directory matching '$HOME/wrkr-*'
       NWORKERS     Program will create N directories starting with '$HOME/wrkr-00000'
  "
}

list_workers() {
  find $HOME -type d -name "master-*"
  find $HOME -type d -name "wrkr-*"

}

cleanup () {

  find $HOME -type d -name "wrkr-*" -print0 2>/dev/null| while IFS= read -r -d '' worker_dir
  do
    rm -rf $worker_dir
    echo "Removed '$worker_dir'."
  done

  find $HOME -type f -name "wrkr-*.log" -print0 2>/dev/null | while IFS= read -r -d '' log_file
  do
    rm $log_file
    echo "Removed '$log_file'."
  done

  find $HOME -type d -name "master-*" -print0 2>/dev/null| while IFS= read -r -d '' master_dir
  do
    rm -rf $master_dir
    echo "Removed '$master_dir'"
  done

  find $HOME -type f -name "master-*.log" -print0 2>/dev/null | while IFS= read -r -d '' master_log
  do
    rm $master_log
    echo "Removed '$master_log'"
  done

}


setup_workers() {

  NWORKERS=$1

  # Check that the argument supplied can be converted to an integer...
  python -c "int($NWORKERS)" > /dev/null 2>&1
  if [[ $? -ne 0 ]]
  then
    usage
    echo "ERROR: '$NWORKERS' cannot be converted to an integer!"
    exit -1
  fi

  echo "Will attempt to create directory structure for $NWORKERS workers and one master..."
  if [[ $NWORKERS -gt 25 ]]
  then
    echo "I refuse. Thats too many directories to create!"
    exit -1
  fi

  for (( i=0; i <= $NWORKERS; ++i ))
  do
    printf -v ZPNUM "%05d" $i # Zero padded number
    FULL_SPATH="$HOME/wrkr-$ZPNUM"

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

  mv "$HOME/wrkr-00000" "$HOME/master-00000"
}

start_workers() {

  find $HOME -type d -name "master-*" -print0 | while IFS= read -r -d '' master_dir
  do
    echo "$master_dir"
    echo "$HOME/master-00000"
    # if [[ "$master_dir" -ne  "$HOME/master-00000" ]]
    # then
    #   echo "Something is wrong! There should not be any other master directories present!"
    #   exit -1
    # fi
    BN=$(basename "$master_dir")
    cd "$master_dir" && pestpp tussock_full.pst /H :5050 > "$HOME/$BN.log" 2>&1 &
  done

  # look for wrkr-* directories
  find $HOME -type d -name "wrkr-*" -print0 |  while IFS= read -r -d '' worker_dir
  do
    BN=$(basename "$worker_dir")
    cd "$worker_dir" && pestpp tussock_full.pst /H localhost:5050 > "$HOME/$BN.log" 2>&1 &
    PID=$!
    echo "Started worker with pid=$PID in: '$worker_dir'"
  done
}


NWORKERS=
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

  --start )         start_workers
                    exit 0
                    ;;

  *)                NWORKERS=$1
                    setup_workers $NWORKERS
                    ;;
esac

