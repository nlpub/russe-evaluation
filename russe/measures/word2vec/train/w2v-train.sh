#!/bin/bash

INPUT=$1
MINCNT=5
for SIZE in 500; do
  for ITER in 3 ; do
    for WINDOW in 10 ; do
      for CBOW in 0 ; do
        
          OUTPUT=$INPUT-sz$SIZE-w$WINDOW-cb$CBOW-it$ITER-min$MINCNT".w2v"
          (time ./word2vec_c/word2vec -train $INPUT -cbow $CBOW -size $SIZE -window $WINDOW -iter $ITER -negative 10 -hs 0 -sample 1e-5 -threads 32 -binary 1 -min-count $MINCNT -output $OUTPUT) 2>$OUTPUT.err
      
      done;
    done;
  done;
done;
