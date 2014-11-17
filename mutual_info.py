import sys
import csv
csv.field_size_limit(sys.maxsize)
import time
from collections import defaultdict
import math

class MutualInfo:
    INPUTFILE_PAIRS = 'input_pairs.txt'
    INPUTFILE_FREQUENCY = 'frequency_list.txt'
    WW_NUM = 100000  # calculated by wc -l for 'input_pairs.txt'
    W_NUM = 100000  # calculated by wc -l for 'frequency_list.txt'

    def __init__(self):
        self.pairs_file_name = self.INPUTFILE_PAIRS
        self.frequency_file_name = self.INPUTFILE_FREQUENCY
        self.fd = defaultdict(dict)


    def get_freq_dict(self, filename):

        t0 = time.time()
        print("Start freq dict")
        counter = 0
        with open(filename, 'r') as csvfile:
            datareader = csv.reader(csvfile, delimiter=' ')
            for ln, row in enumerate(datareader):
                self.fd[row[0]] = row[1]

        t1 = time.time()
        print("Finished. Get input dictionary - time %2.2f secs, whoosh !" % (t1 - t0))


    def calculate_MI(self, filename):

        t0 = time.time()
        counter = 0
        with open(filename, 'r') as csvfile:
            datareader = csv.reader(csvfile, delimiter=',')
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
                px = self.fd.get(word1, 1)/self.W_NUM
                py = self.fd.get(word2, 1)/self.W_NUM
                final_score = math.log(pxy/(px*py))

                print("%s, %s, %d" % (word1, word2, final_score))

        t1 = time.time()
        print("Finished. Calculate MI time %2.2f secs, whoosh !" % (t1 - t0))


    def process(self):
        self.get_freq_dict(self.frequency_file_name)
        self.calculate_MI(self.pairs_file_name)


if __name__ == '__main__':
    c = MutualInfo()
    t0 = time.time()
    c.process()
    t1 = time.time()
    print("Finished. Total processing time %2.2f secs, whoosh !" % (t1 - t0))
