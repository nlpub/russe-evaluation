import sys
import csv
csv.field_size_limit(sys.maxsize)
import time
from collections import defaultdict
import math


DELIMITER = "\t"


class MutualInfo:
    INPUTFILE_PAIRS = 'cooccurences.csv'
    INPUTFILE_FREQUENCY = 'freq.csv'

    def __init__(self):
        self.pairs_file_name = self.INPUTFILE_PAIRS
        self.frequency_file_name = self.INPUTFILE_FREQUENCY
        self.fd = defaultdict(dict)
        self.WW_NUM =  float(self.file_len(self.INPUTFILE_PAIRS)) # 265058510 

    @staticmethod
    def file_len(fname):
        with open(fname) as f:
            for i, l in enumerate(f):
                pass
        return i + 1

    def get_freq_dict(self, filename):

        t0 = time.time()
        print("Start freq dict", file=sys.stderr)
        with open(filename, 'r') as csvfile:
            datareader = csv.reader(csvfile, delimiter=DELIMITER)
            for ln, row in enumerate(datareader):
                self.fd[row[0]] = float(row[1])

        t1 = time.time()
        print("Finished. Get input dictionary - time %2.2f secs, whoosh !" % (t1 - t0), file=sys.stderr)
        print("#words:", len(self.fd), file=sys.stderr)
        print("#pairs:", self.WW_NUM, file=sys.stderr)


    def calculate_MI(self, filename):

        t0 = time.time()
        counter = 0
        with open(filename, 'r') as csvfile:
            datareader = csv.reader(csvfile, delimiter=DELIMITER)
            first_line = True
            for ln, row in enumerate(datareader):
                if first_line:
                    first_line = False
                    continue
                #if counter > 3:
                    #break
                counter += 1
                word1 = row[0]
                word2 = row[1]
                freq = row[2]
                pxy = int(freq)/self.WW_NUM
                px = self.fd.get(word1, 1)/float(len(self.fd))
                py = self.fd.get(word2, 1)/float(len(self.fd))
                #print (">>>", px, py, pxy, px * py, pxy / (px*py), math.log(pxy/(px*py)))
                final_score = math.log(pxy/(px*py))

                print("%s\t%s\t%f" % (word1, word2, final_score))

        t1 = time.time()
        print("Finished. Calculate MI time %2.2f secs, whoosh !" % (t1 - t0), file=sys.stderr)

    def process(self):
        self.get_freq_dict(self.frequency_file_name)
        self.calculate_MI(self.pairs_file_name)


if __name__ == '__main__':
    c = MutualInfo()
    t0 = time.time()
    c.process()
    t1 = time.time()
    print("Finished. Total processing time %2.2f secs, whoosh !" % (t1 - t0), file=sys.stderr)
