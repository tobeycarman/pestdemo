#!/bin/sh

#  08-07-2016
#
#  This finally works. It is not flawless, but it does seem to work. 
#  
#  The general ideas that we will need a separate working directory for 
#  each worker process and a working directory for the master process. Because 
#  we could have potentially hundreds of worker processes, I've made the 
#  setup-workers.sh script to help create all the necessary directories and copy
#  the approporate data to these directories. Then this script will be used by 
#  SLURM to start the PEST++ master and worker processes in the respective 
#  directories.
#   
#  Note: As of 11/07/2016, it is preferable to use /atlas_scratch/$USER as your 
#        "home" working directory for the following workflow.
#  
#  General setup
#  -------------
#  0. Make sure you have PEST++ installed, and accessible on your path. On atlas
#     for me that requires remembering to set some environment variables and 
#     load the pest module on atlas. It is actually helpful to do this after
#     compiling dvmdostem, as PEST++ needs the GCC5.3 module, and that conflicts
#     with the dvmdostem compilation.
#  1. Setup dvmdostem in your home directory; make sure you have checked out the
#     desired git version, and compiled the code.
#  2. Setup the pestdemo repo in your home directory, make desired subdirectory
#     for the calibration case, (e.g. "tussock_full"), and collect the 
#     appprpriate the files. This might require going thru
#     the entire PEST setup process if you are starting from scratch.
#  
#  SLURM batch job setup
#  ---------------------
#  
#  0. Should be done by the last step of the general setup above, but basically, 
#     make sure you have your pest control file (.pst), pest template file, 
#     (.tpl), pest instruction file (.ins), and the helper script 
#     (pest-helper.py) files setup as you want them.
#  
#  1. Make sure you have the wrapper script setup as you want (number of years 
#     to run, etc).
#  
#  2. Modify the dvmdostem config file. The key is that the parameters and 
#     outputs are sourced from the current directory (relative path in the 
#     config file) while the remainder of the inputs are sourced using absolute 
#     paths to the sample data in your ~/dvm-dos-tem/DATA/ directory. The reason 
#     is that each instance of the model needs to have a place to read/write 
#     custom parameter files (as the parameters are modifed by PEST) and it also 
#     needs a custom place to write output files. To avoid needing to copy the 
#     (potentially voluminous) driving input data, we can simply refer
#     to the single copy in your main ~/dvm-dos-tem directory.
#  
#  3. Figure out how many workers you want to have. It seems like at least as 
#     many as the number of adjustable parameters you have. Depending on how 
#     PEST is setup, it might be advantages to have double the number, because
#     if PEST is calculating with central differences, I think it does 2 runs 
#     for each parameter. Of course this is somewhat limited also by the 
#     computer you are running on. However I don't beleive there are any 
#     problems with different instances running on different cores on the same 
#     node, so on atlas, we have a lot of potential cores.
#  
#  4. Run the setup-workers.sh script to setup all your working directories 
#     (and the master directory).
#  
#  5. Use squeue to find a node that is unused. Edit this script to use this 
#     node.
#  6. Run this script by typing "sbatch job.sh"
#  
#  7. Check on the status using sinfo, squeue, and looking at the log output. 
#     There are a few outputs: 
#      - one log file for each worker
#      - a log file for the master
#      - the slrum-NNNNN.log output file for the job submission.
#  
#  8. (Hopefully not, but it is inevitable in the setup/debugging process) 
#     Cancel the job with scancel <JOBID>
#  
#  9. Wait.
#  
#  10. PEST++ will write all the final info in the master directory. Copy that 
#      info off to some secure place and delete all the worker (and master) 
#      directories with the setup-workers.sh --cleanup
#  

#SBATCH -n 105                # cores
#SBATCH -t 1-13:00:00       # 1 day and 13 hours
#SBATCH --partition main    # The partition 
#SBATCH -J pestpp-cal       # sensible name for the job
#SBATCH -w atlas07,atlas08,atlas09,atlas12

MASTERNODE="atlas07"
NWORKERS=104
WORKING_ROOT="/atlas_scratch/$USER"
CASE_NAME="shrub_full"

# Deal with the master process
echo "Starting master process..."
cd $WORKING_ROOT/master-00000 
srun --partition main --nodelist=$MASTERNODE -n 1 pestpp $CASE_NAME.pst /H :5050 > $WORKING_ROOT/master-00000.log 2>&1 &
echo "The srun exit status was: $?"
echo "Created the master process..."

# Wait, seems to help with making sure workers can connect...
DELAY=30
echo Start: $(date)
echo "Waiting $DELAY seconds for the master to start before starting workers..."
sleep $DELAY
echo End wait: $(date)

# Start all the workers...
for (( i=1; i<=$NWORKERS; ++i ))
do
  printf -v ZPNUM "%05d" $i # Zero padded number...
  cd $WORKING_ROOT/wrkr-$ZPNUM &&
  srun -n 1 --partition main pestpp $CASE_NAME.pst /H $MASTERNODE:5050 > $WORKING_ROOT/wrkr-$ZPNUM.log 2>&1 &
  echo "Started worker number $ZPNUM..."
done

echo "Waiting for everything to complete..."
wait

