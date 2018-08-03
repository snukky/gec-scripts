#!/usr/bin/python

import sys
import os
import math
import random


if len(sys.argv) < 2:
    print "usage: {} corpus [error rate]".format(sys.argv[0])
    exit()
    
corpus = sys.argv[1]
err_rate = None
if len(sys.argv) > 2:
    err_rate = float(sys.argv[2])
    print >>sys.stderr, "Desired error rate: {:.4f}".format(err_rate)

lines = int(os.popen("wc -l {} | grep -Po '^[0-9]+'".format(corpus)) \
    .read().strip())

err_no = 0
cor_sents = []

with open(corpus) as corpus_io:
    for idx, line in enumerate(corpus_io):
        err, cor = line.strip().split("\t")[0:2]
        if err.strip().lower() == cor.strip().lower():
            cor_sents.append(idx)
        else:
            err_no += 1


print >>sys.stderr, "All sentences: {}".format(lines)
print >>sys.stderr, "Erroneous sentences: {}".format(err_no)
cur_rate = err_no / float(lines)
print >>sys.stderr, "Sentence error rate: {:.4f}".format(cur_rate)

if err_rate is None:
    exit()

if err_rate <= cur_rate:
    print >>sys.stderr, "Increasing error rate not supported"
    exit()

del_no = max(0, lines - int(math.floor(err_no / err_rate)))

print >>sys.stderr, "Correct sentences to delete: {}".format(del_no)

rm_sents = random.shuffle(cor_sents)
rm_sents = set(cor_sents[:del_no])

with open(corpus) as corpus_io:
    for idx, line in enumerate(corpus_io):
        if idx not in rm_sents:
            print line,
