#!/bin/bash

# monitor-pestpp-run.sh

# Tobey Carman
# October 2016

WORKING_ROOT="/atlas_scratch/$USER"

usage () {
  echo "Usage:

    ./monitor-pestpp-run.sh [ -h | --help | -w | --workers | -m | --master ]

       -h, --help  Show this message and quit.

       -w, --workers   The program will print the last few lines of every worker's
                   log file.

       -m, --master    The program will use "tail -f" to look at the master's log
                   file.

  "
}

report_workers() {
  for i in $(ls $WORKING_ROOT/wrkr-000*.log)
  do 
    echo "=== $i ===" 
    tail -n 2 $i
    echo "---------------"
    echo ""
  done
}

report_master() {
  tail -f $WORKING_ROOT/master-00000.log
}

# Check that the user supplied at least one argument.
if [[ "$#" -ne 1 ]]
then
  usage
  exit -1
fi

case $1 in

  -h | --help )     usage
                    exit 0
                    ;;

  -w | --workers )       report_workers
                    exit 0
                    ;;

  -m | --master )        report_master
                    exit 0
                    ;;

  *)                usage
                    exit -1
                    ;;
esac


