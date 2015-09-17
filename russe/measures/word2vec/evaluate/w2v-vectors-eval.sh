#!/bin/bash

#wget https://s3-eu-west-1.amazonaws.com/dsl-research/wiki/w2v_export/all.norm-sz100-w10-cb0-it1-min100.w2v
#wget https://s3-eu-west-1.amazonaws.com/dsl-research/wiki/w2v_export/all.norm-sz500-w10-cb0-it3-min5.w2v
DATA=../../../evaluation/test.csv
MORPH="" #"-morph"
for W2V in *.w2v ; do
    ID=$(basename -s .w2v $W2V)$MORPH
    RESDIR=$(dirname $DATA)"/results_export/"$ID
    mkdir -p $RESDIR
    python simcalc.py $MORPH -column sim -output $RESDIR"/test.csv" $W2V $DATA >$RESDIR"/"$ID".stdout" 2>$RESDIR"/"$ID".stderr"
done

