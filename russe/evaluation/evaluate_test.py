#!/usr/bin/env python

from os.path import join, splitext, basename, dirname
from pandas import read_csv, Series
from collections import defaultdict
import argparse
from sys import stderr
from evaluate import hj_evaluation, semantic_relation_classification_evaluation


TEST = True  # if true use *-test.csv for evaulation, else use *-train.csv 
DATA_DIR = "."  # the directory where *-test.csv and *-train.csv lives

HJ_TEST = join(DATA_DIR, "hj-test.csv" if TEST else "hj-train.csv")
RT_TEST = join(DATA_DIR, "rt-test.csv" if TEST else "rt-train.csv")
AE_TEST = join(DATA_DIR, "ae-test.csv" if TEST else "ae-train.csv")
AE2_TEST = join(DATA_DIR, "ae2-test.csv" if TEST else "ae2-train.csv")


def get_test(test_fpath):
    test_df = read_csv(test_fpath, ',', encoding='utf8')
    test = defaultdict(dict)
    for i, r in test_df.iterrows():
        test[r["word1"]][r["word2"]] = r["sim"]

    return test


def create_usim(df_fpath, test_fpath):
    print "golden standard:", df_fpath
    print "test.csv:", test_fpath
    test = get_test(test_fpath)

    df = read_csv(df_fpath, ',', encoding='utf8')

    not_found_num = 0
    usim_lst = []
    for i, r in df.iterrows():
        w1 = r["word1"]
        w2 = r["word2"]
        found = w1 in test and w2 in test[w1]
        usim = test[w1][w2] if found else 0.0
        if not found:
            #print w1, w2
            not_found_num += 1
        usim_lst.append(usim)

    df["usim"] = Series(usim_lst)

    print "not found", not_found_num, "of", i
    print "used", i - not_found_num

    usim_fpath = join(dirname(test_fpath), splitext(basename(df_fpath))[0] + "-usim.csv")
    df.to_csv(usim_fpath, encoding="utf-8", index=False, sep=",")
    print "golden standard + test.csv:", usim_fpath, "\n"

    return usim_fpath


def evaluation(args):
    
    print "test.csv:", args.test_fpath

    hj_fpath = create_usim(HJ_TEST, args.test_fpath)
    rt_fpath = create_usim(RT_TEST, args.test_fpath)
    ae_fpath = create_usim(AE_TEST, args.test_fpath)
    ae2_fpath = create_usim(AE2_TEST, args.test_fpath)

    
    r = {}
    r["hj"] = hj_evaluation(hj_fpath)
    r["aehj"] = hj_evaluation(ae_fpath)
    r["ae2hj"] = hj_evaluation(ae2_fpath)
    r["rt-avep"], r["rt-accuracy"] = semantic_relation_classification_evaluation(rt_fpath)
    r["ae-avep"], r["ae-accuracy"] = semantic_relation_classification_evaluation(ae_fpath)
    r["ae2-avep"], r["ae2-accuracy"] = semantic_relation_classification_evaluation(ae2_fpath)
    print >> stderr, "hj\trt-avep\trt-accuracy\tae-avep\tae-accuracy\tae2-avep\tae2-accuracy"
    print >> stderr, "%(hj).5f\t%(rt-avep).5f\t%(rt-accuracy).5f\t%(ae-avep).5f\t%(ae-accuracy).5f\t%(ae2-avep).5f\t%(ae2-accuracy).5f" % r


def main():
    parser = argparse.ArgumentParser(description='Evaluate from test.csv file.')    
    parser.set_defaults(func=evaluation)
    parser.add_argument('test_fpath', help='Path to test.csv file.')
    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()

