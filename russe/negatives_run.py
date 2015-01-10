from os.path import join
from russe.negatives import generate_negatives

dir_fpath = "/Users/sasha/work/russe/"
freq_fpath = join(dir_fpath, "freq.csv")
pmi_w1_fpath = join(dir_fpath, "w1-pmi.csv")
pmi_fpath = join(dir_fpath, "pmi.csv.gz")

for mc in [2]:
    for f in ["rt-train.csv","ae-train.csv", "ae2-train.csv"]:
        generate_negatives(join(dir_fpath, f), freq_fpath, pmi_w1_fpath, pmi_fpath, mult_coeff=mc)
