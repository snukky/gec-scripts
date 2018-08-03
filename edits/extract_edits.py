#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import argparse

from difflib import SequenceMatcher


def main():
    args = parse_user_args()

    for i, line in enumerate(args.input):
        if args.debug and ((i + 1) % 100000 == 0):
            print >> sys.stderr, "[{}]".format(i + 1)

        err_sent, cor_sent = line.strip().split("\t")
        if err_sent == cor_sent:
            continue

        err_toks = err_sent.split()
        cor_toks = cor_sent.split()

        matcher = SequenceMatcher(None, err_toks, cor_toks)
        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag != 'equal':
                print "{}{}{}".format(' '.join(err_toks[i1:i2]),
                                      args.delimiter,
                                      ' '.join(cor_toks[j1:j2]))


def parse_user_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'input',
        nargs='?',
        type=argparse.FileType('r'),
        default=sys.stdin,
        help="parallel sentences")
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('-d', '--delimiter', default='\t')
    return parser.parse_args()


if __name__ == '__main__':
    main()
