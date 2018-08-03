#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import argparse

from difflib import SequenceMatcher
from collections import defaultdict


def main():
    args = parse_user_args()
    # sub, del, ins, nerr, ncorr, m, mer, //nsub, ndel, nins
    stats = defaultdict(int)

    for i, line in enumerate(args.input):
        err_sent, cor_sent = line.strip().split("\t")
        stats['m'] += 1

        if (i + 1) % 100000 == 0:
            print >>sys.stderr, "[{}]".format(i + 1)

        err_toks = err_sent.split()
        cor_toks = cor_sent.split()
        stats['nerr'] += len(err_toks)
        stats['ncor'] += len(cor_toks)

        if err_sent == cor_sent:
            continue

        stats['mer'] += 1
        matcher = SequenceMatcher(None, err_toks, cor_toks)

        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            # err_tok = ' '.join(err_toks[i1:i2])
            # cor_tok = ' '.join(cor_toks[j1:j2])

            if tag == 'replace':
                stats['sub'] += 1
                stats['nsub'] += (i2 - i1)
            elif tag == 'insert':
                stats['ins'] += 1
                stats['nins'] += (j2 - j1)
            elif tag == 'delete':
                stats['del'] += 1
                stats['ndel'] += (i2 - i1)

    print "== Sentence statistics =="
    print "Sentences     : {}".format(stats['m'])
    print "With errors   : {}".format(stats['mer'])
    print "Correct       : {}".format(stats['m'] - stats['mer'])
    ser = stats['mer'] / float(stats['m'])
    print "SER           : {:.4f}".format(ser)
    print ""

    print "== Edit statistics =="
    num_edits = float(stats['sub'] + stats['del'] + stats['ins'])
    print "Edits         : {}".format(int(num_edits))
    print "Substitutions : {:.4f} ={}".format(stats['sub'] / num_edits, stats['sub'])
    print "Deletions     : {:.4f} ={}".format(stats['del'] / num_edits, stats['del'])
    print "Insertions    : {:.4f} ={}".format(stats['ins'] / num_edits, stats['ins'])
    print ""

    print "== Token statistics =="
    len_edits = float(stats['nsub'] + stats['ndel'] + stats['nins'])
    wer = len_edits / float(stats['ncor'])
    print "Source words  : {}".format(stats['nerr'])
    print "Target words  : {}".format(stats['ncor'])
    print "Substitutions : {:.4f} ={}".format(stats['nsub'] / len_edits, stats['nsub'])
    print "Deletions     : {:.4f} ={}".format(stats['ndel'] / len_edits, stats['ndel'])
    print "Insertions    : {:.4f} ={}".format(stats['nins'] / len_edits, stats['nins'])
    print "WER           : {:.4f}".format(wer)


def parse_user_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', nargs='?', type=argparse.FileType('r'),
                        default=sys.stdin, help="parallel file")
    return parser.parse_args()


if __name__ == '__main__':
    main()
