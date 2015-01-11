#!/usr/bin/env python

import argparse
from pandas import read_csv
from scipy.stats import pearsonr, spearmanr

HJ_FILE = "hj-submission.csv"
SRC_FILE = "src-submission.csv"




def hj_evaluation_args(args):
    return hj_evaluation(args.hj_fpath)


def hj_evaluation(hj_fpath):
    print "======================================================="
    print "Evaluation based on correlations with human judgements"
    print "See Section 1.1 of http://russe.nlpub.ru/task\n"

    print "Input file:", hj_fpath
    hj_df = read_csv(hj_fpath, ',', encoding='utf8')
    print "Spearman's correlation with human judgements:\t%.5f (p-value = %.3f)" % spearmanr(hj_df.usim, hj_df.sim)
    print "Pearson's correlation with human judgements:\t%.5f (p-value = %.3f)" % pearsonr(hj_df.usim, hj_df.sim)

    return spearmanr(hj_df.usim, hj_df.sim)[0]


def semantic_relation_classification_evaluation_args(args):
    return semantic_relation_classification_evaluation(args.src_fpath)


def semantic_relation_classification_evaluation(src_fpath):
    print "======================================================="
    print "Evaluation based on semantic relation classificaton"
    print "See Section 1.2 of http://russe.nlpub.ru/task\n"

    raise NotImplementedError()


def main():
    parser = argparse.ArgumentParser(description='RUSSE Evaluation Script. See http://russe.nlpub.ru for more details.')	
    subparsers = parser.add_subparsers(description='Help for subcommand.')
    parser_hj = subparsers.add_parser('hj', description='Evaluation based on correlations with human judgements.')
    parser_hj.set_defaults(func=hj_evaluation_args)
    parser_hj.add_argument('--hj_fpath', help='A CSV file in the format "word1,word2,hj,sim" e.g. ' + HJ_FILE, default=HJ_FILE)

    parser_hj = subparsers.add_parser('src', description='Evaluation based on semantic relation classification.')
    parser_hj.set_defaults(func=semantic_relation_classification_evaluation_args)
    parser_hj.add_argument('--src_fpath', help='A CSV file in the format "word1,word2,related,sim" e.g. ' + SRC_FILE, default=SRC_FILE)

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
