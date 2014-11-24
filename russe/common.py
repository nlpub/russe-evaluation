import pandas as pd
import codecs
from os.path import splitext
from pandas import read_csv
from collections import defaultdict
import re
from pymystem3 import Mystem

# dependenies to the dsl nlp repository
from nlp.common import wc
from nlp.patterns import re_numbers

_mystem = Mystem()


def get_pos(text):
    pos = map(lambda x: x[1], analyze_simple(text))
    if pos is None or len(pos) == 0:
        return ["?"]
    else:
        return pos


def analyze_simple(text):
    res = _mystem.analyze(text)
    out = []
    for r in res:
        if "analysis" not in r or "text" not in r: continue
        if len(r["analysis"]) < 1 or "lex" not in r["analysis"][0] or "gr" not in r["analysis"][0]:
            out.append((r["text"], "?"))
        else:
            pos = re.split('=|,', r["analysis"][0]["gr"])[0] 
            out.append((r["analysis"][0]["lex"], pos))
    return out


def sort_pairs(input_fpath):
    df = read_csv(input_fpath, ',', encoding='utf8')
    df = df.sort(['word1', 'sim'], ascending=[1, 0])

    output_fpath = splitext(input_fpath)[0] + "-sort.csv"
    df.to_csv(output_fpath, sep=',', encoding='utf-8', index=False)
    print "sorted:", output_fpath

    return output_fpath


def simmetrize(pairs_fpath):
    output_fpath = splitext(pairs_fpath)[0] + "-sym.csv"
    rels = defaultdict(dict)
    pairs = pd.read_csv(pairs_fpath, ',', encoding='utf8')
    
    for i, row in pairs.iterrows():
        if "word1" in row and "word2" in row and "sim" in row:
            value_dir = {"sim": row["sim"]}
            value_inv = {"sim": row["sim"]}
            if "dir" in row and "inv" in row:
                value_dir["dir"] = row["dir"]
                value_dir["inv"] = row["inv"]
                value_inv["dir"] = row["inv"]
                value_inv["inv"] = row["dir"]
            rels[row["word1"]][row["word2"]] = value_dir
            rels[row["word2"]][row["word1"]] = value_inv
        else:
            continue

    with codecs.open(output_fpath, "w", "utf-8") as output_file:
        print >> output_file, "word1,word2,sim,dir,inv"

        for i, w1 in enumerate(rels):
            #if i > 100: break
            for w2 in rels[w1]:
                print >> output_file, "%s,%s,%s,%s,%s" % (
                    w1, w2, rels[w1][w2]["sim"], rels[w1][w2]["dir"], rels[w1][w2]["inv"])

    print "simmetrized file:", output_fpath

    return output_fpath


def sample_pairs(pairs_fpath, test_each=2, extended=False):
    test_fpath = splitext(pairs_fpath)[0] + "-test.csv"
    train_fpath = splitext(pairs_fpath)[0] + "-train.csv"
  
    pairs = pd.read_csv(pairs_fpath, ',', encoding='utf8')
    
    with codecs.open(test_fpath, "w", "utf-8") as test, codecs.open(train_fpath, "w", "utf-8") as train:
        if extended:
            print >> test, "word1,word2,sim,dir,inv"
            print >> train, "word1,word2,sim,dir,inv"
        else:
            print >> test, "word1,word2,sim"
            print >> test, "word1,word2,sim"
        
        prev = "*"
        stim_num = 0
        train_pairs = 0
        test_pairs = 0
        train_stim = 0
        test_stim = 0

        for i, row in pairs.iterrows():
            if row["word1"] != prev:
                stim_num += 1
                if stim_num % test_each == 0: test_stim += 1
                else: train_stim += 1
            prev = row["word1"]

            if stim_num % test_each == 0:
                out = test
                test_pairs += 1
            else:
                out = train
                train_pairs += 1

            if extended:
                print >> out, "%s,%s,%s,%s,%s" % (row["word1"], row["word2"], row["sim"], row["dir"], row["inv"])
            else:
                print >> out, "%s,%s,%s" % (row["word1"], row["word2"], row["sim"])
            
    print "TEST"
    print "file:", test_fpath
    print "#pairs:", wc(test_fpath)
    print "#stimuls:", test_stim

    print "\nTRAIN"
    print "file:", train_fpath
    print "#pairs:", wc(train_fpath)
    print "#stimuls:", train_stim


def process_associations(ae_fpath, ae_stat_fpath):
    ae = pd.read_csv(ae_fpath, ',', encoding='utf8')
    print "#pairs:", len(ae)
    ae_stat = pd.read_csv(ae_stat_fpath, ',', encoding='utf8')

    words2drop = {row["word"]: row["num_ge3"] for i, row in ae_stat.iterrows()}
    print "#word1:", len(words2drop)
    words2drop = {word: words2drop[word] for word in words2drop if words2drop[word] < 9}
    print "#word2drop:", len(words2drop)

    pairs2drop = [i for i, row in ae.iterrows() if row["word1"] in words2drop]
    print "#pairs2drop:", len(pairs2drop)
    ae = ae.drop(pairs2drop)
    print "#pairs final:", len(ae)

    ae_out_fpath = splitext(ae_fpath)[0] + ".out.csv"
    ae.to_csv(ae_out_fpath, sep=',', encoding='utf-8', index=False)
    print "saved to:", ae_out_fpath

    test_fpath = splitext(ae_fpath)[0] + ".test.csv"
    train_fpath = splitext(ae_fpath)[0] + ".train.csv"

    with codecs.open(test_fpath, "w", "utf-8") as test, codecs.open(train_fpath, "w", "utf-8") as train:
        print >> test, "word1,word2,sim"
        print >> train, "word1,word2,sim"

        prev = "*" 
        stim_num = 0
        train_pairs = 0
        test_pairs = 0
        train_stim = 0
        test_stim = 0

        for i, row in ae.iterrows():
            if row["word1"] != prev: 
                stim_num += 1
                if stim_num % 2 == 0: test_stim += 1
                else: train_stim += 1
            prev = row["word1"]

            if  " " in row["word2"] or re_numbers.search(row["word2"]): continue
            if stim_num % 2 == 0:
                out = test
                test_pairs += 1
            else:
                out = train
                train_pairs += 1
            print >> out, "%s,%s,%d" % (row["word1"], row["word2"], row["sim"])

    print "test:", test_fpath
    print "test pairs:", wc(test_fpath)
    print "test stim:", test_stim

    print "train:", train_fpath
    print "train pairs:", wc(train_fpath)
    print "train stim:", train_stim


# YARN stuff

def get_synsets(yarn_fpath, synset_fpath):
    
    # ToDo: add filter by number of words in synset by freq
    
    words = read_csv(yarn_fpath, ',', encoding='utf8')
    synsets = defaultdict(set)
    with codecs.open(synset_fpath, "w", "utf-8") as synset_file:
        prev_id = -1
        for i, row in words.iterrows():
            synsets[row.synset_id].add(row.word)
        
            if prev_id != -1 and row.synset_id != prev_id:
                print >> synset_file, "\n"
            else:
                print >> synset_file, "%s," % row.word,
            prev_id = row.synset_id
            
    return synsets


def generate_synonyms(synsets, output_fpath, symmetric=True, spaser=False):
    with codecs.open(output_fpath, "w", "utf-8") as output_file:
        print >> output_file, "word1,word2,sim"
        for s in synsets:
            for i, wi in enumerate(synsets[s]):
                for j, wj in enumerate(synsets[s]):
                    if not symmetric and i > j:
                        print >> output_file, "%s,%s,syn" % (wi, wj)
                    elif i != j:
                        print >> output_file, "%s,%s,syn" % (wi, wj)
            if spaser: print >> output_file, ""

    print "synonyms:", output_fpath
