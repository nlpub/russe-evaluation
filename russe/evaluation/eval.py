#!/usr/bin/env python

import argparse
from pandas import read_csv
from scipy.stats import pearsonr, spearmanr
from os.path import splitext
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import average_precision_score, precision_recall_curve, \
    accuracy_score, roc_auc_score, classification_report

HJ_FILE = "hj-submission.csv"
SRC_FILE = "src-submission.csv"
SHOW = False


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
    print "\n======================================================="
    print "Evaluation based on semantic relation classificaton"
    print "See Section 1.2 of http://russe.nlpub.ru/task\n"

    y_test, y_predict, y_score = predict_by_sim(src_fpath)
    s = src_evaluation(y_test, y_predict, y_score, src_fpath)

    return s


def src_evaluation(y_test, y_predict, y_score, src_fpath, print_data=False):
    if print_data:
        print_y(y_test, y_score)
    
    # Compute performance metrics
    s = {}
    precision, recall, _ = precision_recall_curve(y_test, y_score)
    s["average_precision"] = average_precision_score(y_test, y_score)
    s["roc_auc"] = roc_auc_score(y_test, y_score)
    s["accuracy"] = accuracy_score(y_test, y_predict)
    
    for statistic in s:
        print "%s: %.3f" % (statistic, s[statistic])
        
    print classification_report(y_test, y_predict)
    
    # Plot Precision-Recall curve
    plt.clf()
    plt.plot(recall, precision, label='Precision-Recall curve')
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.ylim([0.0, 1.05])
    plt.xlim([0.0, 1.0])
    plt.title('Precision-Recall curve: AUC={0:0.5f}'.format(s["average_precision"]))
    if SHOW: plt.show()
    fig_fpath = splitext(src_fpath)[0] + "-pr.png"
    plt.savefig(fig_fpath)
    print "precision-recall plot:", fig_fpath

    return s["average_precision"]


def print_y(y_test, y_score):
    y_test = np.reshape(y_test, (y_test.shape[0], 1))
    y_score = np.reshape(y_score, (y_score.shape[0], 1))
    y = np.hstack([y_test, y_score])
    print y[y[:,1].argsort()][::-1]


def predict_by_sim(df_fpath):
    df = read_csv(df_fpath, ',', encoding='utf8', error_bad_lines=False, warn_bad_lines=False)
    df = df.sort(['word1', 'usim'], ascending=[1, 0])
    
    df_group = df.groupby(["word1"], sort=False).count()
    rel_num = {r.name: r.word2 for i, r in df_group.iterrows()}
    
    y_predict = []
    w_i = 1
    w_prev = ""
        
    for i, r in df.iterrows():
        if r.word1 != w_prev: w_i = 1
        related = int(w_i <= float(rel_num[r.word1]) / 2)
        y_predict.append(related)
        
        w_i += 1
        w_prev = r.word1
    
    df["predict"] = y_predict
    output_fpath = splitext(df_fpath)[0] + "-predict.csv"
    df.to_csv(output_fpath, sep=',', encoding='utf-8', index=False)
    print "predict:", output_fpath
    
    y_test = df.sim.values.tolist()
    y_predict = df.predict.values.tolist()
    y_score = df.usim.values.tolist()
    
    return y_test, y_predict, y_score


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
