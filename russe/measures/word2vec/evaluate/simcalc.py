#!/usr/bin/env python
# coding=utf8

from sys import stderr
import csv
import argparse
import os
import logging
from utils import load_vectors

logger = logging.getLogger("gensim.models.word2vec")

def get_word_variants(word, prefix2word):
    word = word.replace(u' ', u'_').replace(u'-', u'_').strip()
    res = set()
    res.add(word)
    res.add(word.replace(u'ё', u'е'))

    prefix = word.split(u'_')[0]
    if prefix in prefix2word:
        res.update(prefix2word[prefix])

    return res


def get_word_variants_morph(word, vectors, logfile):
    print >> logfile, ("WARNING: splitting word %s" % word).encode('utf-8')
    res = set()
    word = word.replace(u' ', u'_').replace(u'-', u'_').strip()
    for w in word.split(u'_'):
        if w in vectors:
            res.add(w)

    if len(res) != 0:
        return res

    for i in xrange(int(2*len(word)/3)):
        part1 = word[i+1:]
        if part1 in vectors:
            res.add(part1)

    return res


def sim(vectors, prefix2word, word1, word2, logfile, morph_hack):
    options1 = get_word_variants(word1, prefix2word)
    options2 = get_word_variants(word2, prefix2word)


    if morph_hack and len([x for x in options1 if x in vectors]) == 0:
        options1 = get_word_variants_morph(word1, vectors, logfile)
    if morph_hack and len([x for x in options2 if x in vectors]) == 0:
        options2 = get_word_variants_morph(word2, vectors, logfile)

    (res, best1, best2) = (None, None, None)
    for w1 in options1:
        for w2 in options2:
            if w1 in vectors and w2 in vectors:
                newres = vectors.similarity(w1, w2)
                if res is None or newres > res:
                    (res, best1, best2) = (newres, w1, w2)

    s = []
    for (options, best) in [(options1, best1), (options2, best2)]:
        s.append('|'.join(('!' if x == best else '+' if x in vectors else '-') + x for x in options))

    if res is None:
        print >> logfile, ("ERROR: <%s>,<%s>\tsim(%s, %s)" % (word1, word2, s[0], s[1])).encode('utf-8')
    else:
        print >> logfile, ("<%s>,<%s>\t%f = sim(%s, %s)" % (word1, word2, res, s[0], s[1])).encode('utf-8')

    return res if res is not None else 0.0


def main():
    parser = argparse.ArgumentParser(
        description='Calculates semantic similarity for each pair of words in the specified input file and saves result '
                    'to the output file. Uses specified word2vec word vectors file.')
    parser.add_argument('vectors', help='word2vec word vectors file.', default='')
    parser.add_argument('input', help='Input file in csv format (with comma as separator). Each line is a pair of words, '
                                      'for which similarity is calculated.', default='')
    parser.add_argument('-output', help='Output file in csv format (with comma as separator).', default='')
    parser.add_argument('-column', help="Name of the output column. If column doesn't exist, it will be added, otherwise "
                                        "data in existing column will be modified.", default='res')
    parser.add_argument('-morph', help="Enable morphology hack.", action='store_true')
    args = parser.parse_args()

    fvec = args.vectors
    fin = args.input
    fout = fin + '-' + os.path.basename(fvec) if args.output == '' else args.output
    cout = args.column
    morph_hack = args.morph

    print >> stderr, "Loading vectors from {}".format(fvec)
    vectors = load_vectors(fvec)

    # for words with underscore (ex: берег_v, берег_s, северо_запад, вода_и_медные_трубы)
    prefix2word = {}
    for x in vectors.vocab.iterkeys():
        if '_' not in x:
            continue
        prefix = x.split('_')[0]
        if prefix not in prefix2word:
            prefix2word[prefix] = [x]
        else:
            prefix2word[prefix].append(x)

    # for e in prefix2word.iteritems():
    #     if len(e[1]) > 1:
    #         print >> stderr, ("%s: %s" % (e[0], ':'.join(e[1]))).encode('utf-8')

    print >> stderr, "Calculating similarity for {}; writing result to {}".format(fin, fout)
    with open(fin, 'r') as input_file, open(fout, "w") as output_file, open(fout+'.log', "w") as log_file:
        inp = csv.DictReader(input_file, delimiter=',', quoting=csv.QUOTE_MINIMAL, quotechar="'")
        # inp_fieldnames = inp.fieldnames
        out_fieldnames = inp.fieldnames if cout in inp.fieldnames else inp.fieldnames + [cout]
        out = csv.DictWriter(output_file, out_fieldnames, delimiter=',', quoting=csv.QUOTE_MINIMAL, quotechar="'")
        out.writeheader()
        for linenum, ex in enumerate(inp):
            if linenum % 1000 == 0:
                    print 'Lines processed: {}'.format(linenum)

            ex[cout] = sim(vectors, prefix2word, ex['word1'].decode('utf-8'), ex['word2'].decode('utf-8'), log_file, morph_hack)
            out.writerow(ex)


if __name__ == '__main__':
    main()
