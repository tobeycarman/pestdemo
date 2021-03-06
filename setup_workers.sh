#!/bin/bash

# Helper script for parallel PEST run.

# Tobey Carman
# July 2016

#WORKING_ROOT="$HOME"
WORKING_ROOT="/atlas_scratch/$USER"

usage () {
  echo "Usage:

    ./setup_workers.sh [ -h | --help | --cleanup | N EXPERIMENT_CASE ]

       -h, --help  Show this message and quit.
       --list      Show info about any existing worker and master directories

       --cleanup   The program will delete all directories and log files matching
                     '$WORKING_ROOT/wrkr-*'
                     '$WORKING_ROOT/master-*'
                     '$WORKING_ROOT/wrkr-*.log'
                     '$WORKING_ROOT/master-*.log'

       --start     The program will start a worker in each directory matching 
                     '$WORKING_ROOT/wrkr-*'
                   NOTE: For use on computers that don's have SLURM; if your computer 
                   uses SLRUM, then submit via sbatch!

       N EXPERIMENT_CASE
                   The program will create N directories for EXPERIMENT_CASE and
                   will copy files from the main dvm-dos-tem directory and the
                   EXPERIMENT_CASE directory into the master and worker directories.
                   The directories will start with:
                     '$WORKING_ROOT/master-00000' and
                     '$WORKING_ROOT/wrkr-00001'

  "
}

list_workers () {
  find $WORKING_ROOT -type d -name "master-*"
  find $WORKING_ROOT -type d -name "wrkr-*"
}

cleanup () {

  find $WORKING_ROOT -type d -name "wrkr-*" -print0 2>/dev/null | while IFS= read -r -d '' worker_dir
  do
    rm -rf $worker_dir
    echo "Removed '$worker_dir'"
  done

  find $WORKING_ROOT -type f -name "wrkr-*.log" -print0 2>/dev/null | while IFS= read -r -d '' log_file
  do
    rm $log_file
    echo "Removed '$log_file'"
  done

  find $WORKING_ROOT -type d -name "master-*" -print0 2>/dev/null | while IFS= read -r -d '' master_dir
  do
    rm -rf $master_dir
    echo "Removed '$master_dir'"
  done

  find $WORKING_ROOT -type f -name "master-*.log" -print0 2>/dev/null | while IFS= read -r -d '' master_log
  do
    rm $master_log
    echo "Removed '$master_log'"
  done

}


setup_workers() {

  NWORKERS=$1
  EXPERIMENT_CASE=${2%/} # <-- strips trailing slash, apparently posix compliant

  # Check that user supplied enough args
  if [[ "$#" -ne 2 ]]
  then
    usage
    echo "ERROR: You must supply 2 args (number of directories, and experiment case directory)!"
    exit -1
  fi

  # Check that the 1st argument supplied can be converted to an integer...
  python -c "int($NWORKERS)" > /dev/null 2>&1
  if [[ $? -ne 0 ]]
  then
    usage
    echo "ERROR: '$NWORKERS' cannot be converted to an integer!"
    exit -1
  fi

  # Check that the 2nd argument supplied is a valid directory
  if [[ ! -d "$2" ]]
  then
    usage
    echo "ERROR: $2 is not a valid directory for your 'experiment case'!"
    exit -1
  fi

  echo "Will attempt to create directory structure for $NWORKERS workers and one master..."
  if [[ $NWORKERS -gt 99999 ]]
  then
    echo "Can't create more than 99999 directories without changing the naming pattern."
    exit -1
  fi

  for (( i=0; i <= $NWORKERS; ++i ))
  do
    printf -v ZPNUM "%05d" $i # Zero padded number
    FULL_SPATH="$WORKING_ROOT/wrkr-$ZPNUM"

    mkdir -p $FULL_SPATH
    mkdir -p $FULL_SPATH/config && cp -r $WORKING_ROOT/dvm-dos-tem/config $FULL_SPATH/
    mkdir -p $FULL_SPATH/parameters && cp -r $WORKING_ROOT/dvm-dos-tem/parameters $FULL_SPATH/
    mkdir -p $FULL_SPATH/output
    #cp $WORKING_ROOT/dvm-dos-tem/DATA/Toolik_10x10_allyrs/output/* $FULL_SPATH/output
    cp $WORKING_ROOT/pestdemo/$EXPERIMENT_CASE/$EXPERIMENT_CASE.pst $FULL_SPATH
    cp $WORKING_ROOT/pestdemo/$EXPERIMENT_CASE/cmt_calparbgc.tpl $FULL_SPATH
    cp $WORKING_ROOT/pestdemo/$EXPERIMENT_CASE/dvmdostem-pest-wrapper.sh $FULL_SPATH
    cp $WORKING_ROOT/pestdemo/$EXPERIMENT_CASE/read-simple-outputs.ins $FULL_SPATH
    cp $WORKING_ROOT/pestdemo/pest-helper.py $FULL_SPATH

  done

  echo "Rename worker-00000 to master-00000"
  mv "$WORKING_ROOT/wrkr-00000" "$WORKING_ROOT/master-00000"
}

start_workers() {
  echo "WARNING WARNING WARNING!!!!"
  echo "This functionlaity likely needs refactoring to accomodate the change to keeping"
  echo "the pest-helper.py and other scripts at the root of the pestdemo repo!!"
  echo ""
  find $WORKING_ROOT -type d -name "master-*" -print0 | while IFS= read -r -d '' master_dir
  do
    echo "$master_dir"
    echo "$WORKING_ROOT/master-00000"
    # if [[ "$master_dir" -ne  "$WORKING_ROOT/master-00000" ]]
    # then
    #   echo "Something is wrong! There should not be any other master directories present!"
    #   exit -1
    # fi
    BN=$(basename "$master_dir")
    cd "$master_dir" && pestpp tussock_full.pst /H :5050 > "$WORKING_ROOT/$BN.log" 2>&1 &
  done

  # look for wrkr-* directories
  find $WORKING_ROOT -type d -name "wrkr-*" -print0 |  while IFS= read -r -d '' worker_dir
  do
    BN=$(basename "$worker_dir")
    cd "$worker_dir" && pestpp tussock_full.pst /H localhost:5050 > "$WORKING_ROOT/$BN.log" 2>&1 &
    PID=$!
    echo "Started worker with pid=$PID in: '$worker_dir'"
  done
}


NWORKERS=
# Check that user supplied exactly one argument
if [[ "$#" -lt 1 ]]
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
                    EXPERIMENT=$2
                    setup_workers $NWORKERS $EXPERIMENT
                    ;;
esac

