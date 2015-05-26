#!/bin/bash

echo "Downloading and compiling word2vec ..."
svn checkout http://word2vec.googlecode.com/svn/trunk/ ./word2vec_c || { echo "Couldn't download word2vec source code: check SVN is installed and works properly."; exit 1; }
cd word2vec_c && make && cd .. || { echo "Couldn't compile word2vec source code: check gcc and make are installed, look above for errors description."; exit 1; }

echo $'\n\nDownloading plaintext version of Wikipedia ...'
WIKI_URL=https://s3-eu-west-1.amazonaws.com/dsl-research/wiki/wiki-ru-noxml.txt.bz2
wget $WIKI_URL || { echo "Couldn't download plaintext version of Wikipedia from $WIKI_URL : check if this URL is available. "; exit 1; }

echo $'\n\nPreprocessing corpus ...'
bzcat wiki-ru-noxml.txt.bz2 | pv -s 3171521092 | train/w2v-preprocess-plaintext.sh wiki-ru-noxml.txt > wiki_raw.norm || { echo "Couldn't preprocess corpus: look above for errors description."; exit 1; }

echo $'\n\nTraining word2vec model ...'
train/w2v-train.sh wiki_raw.norm || { echo "Couldn't train word2vec model: look above for errors description."; exit 1; }
