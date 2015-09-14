word2vec skip-gram model for Russian language 
--------------------------------------------

Model trained on librusec with window size 10, vector dimensionality 500, 3 iterations, skip gram method can be downloaded from:
https://s3-eu-west-1.amazonaws.com/dsl-research/wiki/w2v_export/all.norm-sz500-w10-cb0-it3-min5.w2v

Distributional Thesaurus of Russian language constructed based on this model:

https://s3-eu-west-1.amazonaws.com/dsl-research/distrib_thes/3attempt/all.norm-sz500-w10-cb0-it3-min5.w2v.vocab_1100000_similar250.gz

You can train model on Wikipedia using script w2v-wiki-train.sh
