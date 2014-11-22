import codecs
from pymystem3 import Mystem
import sys 
from time import time
from nlp.common import PrettyPrinterUtf8 as pp
import json
import re
import traceback 

""" Genaration of a POS tagged corpus in the CoNLL format. """

output_fpath = sys.argv[1] if len(sys.argv) > 1 else "output.txt"

tic = time()
with codecs.open(output_fpath, "w", "utf-8") as output:
    m = Mystem()
    i = 0 
    for line in sys.stdin:
        try: 
            i += 1
            if i % 1000 == 0: print i
            f = line.split("\t")
            url, title, text = f[0], f[1], ' '.join(f[2:])
     
            print >> output, "<doc url='%s' title='%s'>" % (url, title.decode("utf-8"))
            res = m.analyze(text)
            for r in res:
                if "analysis" not in r or "text" not in r: continue
     
                if len(r["analysis"]) < 1 or "lex" not in r["analysis"][0] or "gr" not in r["analysis"][0]:
                    print >> output, "%s\t%s\t%s" % (r["text"], r["text"], "?") 
                else:
                    pos = re.split('=|,', r["analysis"][0]["gr"])[0] 
                    print >> output, "%s\t%s\t%s" % (r["text"], r["analysis"][0]["lex"], pos)
            print >> output, "</doc>"
        except:
            print "Bad line: '%s'" % line
            print "Error:", traceback.format_exc()
            print "Fields num:", len(line.split("\t"))
print "Elapsed:", time() - tic, "sec."

