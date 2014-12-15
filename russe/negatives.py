from pandas import read_csv
from nlp.common import prt
from time import time
from nlp.common import exists
import cPickle as pickle
import gzip
import codecs
from os.path import splitext, join
from collections import Counter
from nlp.morpho.mystem import get_pos
from collections import defaultdict

rt_fpath = "/home/ubuntu/russe/annotate/rt-test.csv"
ae_fpath = "/home/ubuntu/russe/annotate/ae-test.csv"
ae2_fpath = "/home/ubuntu/russe/annotate/ae2-test.csv"
freq_fpath = "/home/ubuntu/russe/freq.csv"
pmi_w1_fpath = "/home/ubuntu/russe/w1-pmi.csv"
pmi_fpath = "/home/ubuntu/russe/pmi.csv.gz" # 265058509 lines

MAX_PMI = -0.02
MIN_LEN = 3
MULT_COEFF = 2


def generate_negatives(relations_fpath, freq_fpath, pmi_w1_fpath, pmi_fpath, mult_coeff=MULT_COEFF):
    tic = time()

    output_fpath = splitext(relations_fpath)[0] + "-out.csv"
    common_fpath = splitext(relations_fpath)[0] + "-common.csv"
    freq_pkl_fapth = freq_fpath + ".pkl"

    pos_df = read_csv(relations_fpath, ',', encoding='utf8')
    rel_freq = Counter([w for w in pos_df.word1])

    if exists(freq_pkl_fapth):
        freq = pickle.load(open(freq_pkl_fapth, "rb"))
    else:
        freq_df = read_csv(freq_fpath, '\t', encoding='utf8')
        freq = {row["word"]: row["freq"] for i, row in freq_df.iterrows()}
        pickle.dump(freq, open(freq_pkl_fpath, "wb"))

    w1_df = read_csv(pmi_w1_fpath, ',', encoding='utf8')
    w1_pmi = {w for w in w1_df.word}

    w1_rel = set(rel_freq.keys())
    common = w1_rel.intersection(w1_pmi)
    print "w1 total:", len(w1_rel)
    print "w1 found:", len(common)

    # save common relations and load them
    idx2del = []
    for i, row in pos_df.iterrows():
        if row.word1 not in common: idx2del.append(i)

    common_df = pos_df.copy()
    common_df.drop(idx2del)
    common_df.to_csv(common_fpath, delimiter=";", encoding="utf-8", index=False)

    positives = defaultdict(list)
    for w1, rows in common_df.groupby(["word1"]):    
        for i, row in rows.iterrows(): positives[w1].append(row.word2)


    # find all related words
    with codecs.open(output_fpath, "w", "utf-8") as out:
        used_words = {}
        out.write("word1;word2;sim;freq\n")
        w1_prev = "" 
        rels = []
        for i, line in enumerate(gzip.open(pmi_fpath, "rb")):
            if i % 1000000 == 0: print i / 1000000

            # is entry good?
            f = line.split("\t")
            w1 = f[0].decode("utf-8")
            if len(f) < 3 or w1 not in common: continue    
            sim = float(f[2])
            w2 = f[1].decode("utf-8")
            if sim > MAX_PMI or w2 not in freq: continue
            pos = get_pos(w2)[0]
            if pos != "S" or len(w2) < MIN_LEN or w2 in used_words: continue

            # good entry                
            if w1 != w1_prev and w1_prev != "":
                print ".",      
                r = {(w,s): freq[w] for w, s in rels}
                i = 0
                rnd_num = mult_coeff * rel_freq[w1_prev]
                for w, s in sorted(r, key=r.get, reverse=True):
                    out.write("%s;%s;%s;%s\n" % (w1_prev, w, s, freq[w]))
                    used_words[w] = 1
                    i += 1
                    if i >= rnd_num: break
                rels = [(w2, sim)]                    
            else:
                rels.append((w2, sim))                    

            w1_prev = w1

    print "elapsed: %d sec." % (time() - tic)
    
    
for x in ["rt-train.csv","ae-train.csv", "ae2-train.csv"]:
    generate_negatives("/home/ubuntu/russe/annotate/" + x, freq_fpath, pmi_w1_fpath, pmi_fpath)    
# generate_negatives(rt_fpath, freq_fpath, pmi_w1_fpath, pmi_fpath)
# generate_negatives(ae2_fpath, freq_fpath, pmi_w1_fpath, pmi_fpath)
# generate_negatives(ae_fpath, freq_fpath, pmi_w1_fpath, pmi_fpath)

