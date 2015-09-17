word2vec skip-gram model for Russian language 
--------------------------------------------

Word vectors for Russian words trained with Word2Vec software on librusec (150G of plaintext) with different parameters:
window size 10, vector dimensionality 500, 3 iterations, skip gram model, words occured at least 5 times (14G):
https://s3-eu-west-1.amazonaws.com/dsl-research/wiki/w2v_export/all.norm-sz500-w10-cb0-it3-min5.w2v
window size 10, vector dimensionality 100, 1 iterations, skip gram model, words occured at least 100 times (500M):
https://s3-eu-west-1.amazonaws.com/dsl-research/wiki/w2v_export/all.norm-sz100-w10-cb0-it1-min100.w2v

To use these vectors in Python please use gensim library and load_vectors() function from evaluate/utils.py. An example of solving RUSSE task using these vectors is in evaluate/simcalc.py and can be executed with evaluate/w2v-vectors-eval.sh

You can also train your own model on Russian Wikipedia (3G of plaintext) using script w2v-wiki-train.sh

If you used any of the provided vectors or scripts, please refer to the following article:
Arefyev N. V., Panchenko A. I., Lukanin A. V., Lesota O. O., Romanov P. V. Evaluating Three Corpus based Semantic Similarity Systems for Russian // Компьютерная лингвистика и интеллектуальные технологии: По материалам ежегодной Международной конференции Диалог (Москва, 27 — 30 мая 2015 г.). Вып. 14 (21). — Т. 2. — Изд-во РГГУ Москва, 2015. — С. 116–128


Distributional Thesaurus of Russian language constructed based on this model:

https://s3-eu-west-1.amazonaws.com/dsl-research/distrib_thes/3attempt/all.norm-sz500-w10-cb0-it3-min5.w2v.vocab_1100000_similar250.gz


