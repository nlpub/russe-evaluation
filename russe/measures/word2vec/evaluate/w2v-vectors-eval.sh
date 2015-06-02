#!/bin/bash

export PYTHONPATH=$PYTHONPATH:/mnt2/home/ubuntu/w2v/treeton/dev/russe
DATA=russe_tasks/test.csv
MORPH="" #"-morph"
for W2V in librusec/all.norm-sz500-*default.w2v ; do
    ID=$(basename -s .w2v $W2V)$MORPH
    RESDIR=$(dirname $DATA)"/results_export/"$ID
    mkdir -p $RESDIR
    treeton/dev/russe/w2v/w2v_simcalc/simcalc.py $MORPH -column sim -output $RESDIR"/test.csv" $W2V $DATA >$RESDIR"/"$ID".stdout" 2>$RESDIR"/"$ID".stderr"
done

