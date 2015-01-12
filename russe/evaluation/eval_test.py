#!/usr/bin/env python

from os.path import join, splitext, basename, dirname
from pandas import read_csv, Series
from collections import defaultdict
import argparse
from sys import stderr
from russe.evaluation.eval import hj_evaluation, semantic_relation_classification_evaluation


TEST_DIR = "/home/sasha/tmp/russe/eval/dataset/test"
HJ_TEST = join(TEST_DIR, "hj-test.csv")
RT_TEST = join(TEST_DIR, "rt-test.csv")
AE_TEST = join(TEST_DIR, "ae-test.csv")
AE2_TEST = join(TEST_DIR, "ae2-test.csv")


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

    print >> stderr, "hj:", hj_evaluation(hj_fpath)
    print >> stderr, "rt:",semantic_relation_classification_evaluation(rt_fpath)
    print >> stderr, "ae:",semantic_relation_classification_evaluation(ae_fpath)
    print >> stderr, "ae2:",semantic_relation_classification_evaluation(ae2_fpath)


def main():
    parser = argparse.ArgumentParser(description='Evaluate from test.csv file.')    
    parser.set_defaults(func=evaluation)
    parser.add_argument('test_fpath', help='Path to test.csv file.')
    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()




