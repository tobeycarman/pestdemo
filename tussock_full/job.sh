#!/bin/sh


#SBATCH -n 74               # cores 
#SBATCH -t 1-03:00:00       # 1 day and 3 hours
#SBATCH --partition main    # The partition 
#SBATCH -J tbc_test_pestpp  # sensible name for the job


cd $HOME/master-00000 
srun --partition main --nodelist="atlas11" -n 1  pestpp tussock_full.pst /H :5050 > $HOME/master-00000.log 2>&1 &

echo "Waiting for the master to start before starting workers..."
sleep 30

NWORKERS=74

for (( i=1; i<=$NWORKERS; ++i ))
do
  printf -v ZPNUM "%05d" $i # Zero padded number...
  cd $HOME/wrkr-$ZPNUM &&
  srun -n 1 --partition main pestpp tussock_full.pst /H atlas11:5050 > $HOME/wrkr-$ZPNUM.log 2>&1 &
  echo "Started worker number $ZPNUM..."
done

echo "Waiting for everything to complete..."
wait

