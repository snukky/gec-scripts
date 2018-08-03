#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import argparse


def main():
    args = parse_user_args()
    seed_patts = load_patterns(args.seed_patterns)
    data_patts = load_patterns(args.data_patterns)

    for min_freq in range(args.min_freq, args.max_freq):
        filt_patts = {k: v for k, v in seed_patts.iteritems() if v >= min_freq}

        count_hits = 0
        count_all = 0
        for patt, freq in data_patts.iteritems():
            if patt in filt_patts:
                count_hits += freq
            count_all += freq

        frac = count_hits / float(count_all)
        print "{}\t{}/{}\t{:.4f}".format(min_freq, count_hits, count_all, frac)


def load_patterns(pattern_io):
    patterns = {}
    for i, line in enumerate(pattern_io):
        pattern, _, freq = line.strip().split("\t")
        patterns[pattern] = int(freq)
    return patterns


def debug(msg):
    print >>sys.stderr, msg


def parse_user_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--seed-patterns',
                        type=argparse.FileType('r'), required=True)
    parser.add_argument('-d', '--data-patterns',
                        type=argparse.FileType('r'), required=True)
    parser.add_argument('--min-freq', type=int, default=1)
    parser.add_argument('--max-freq', type=int, default=10)
    return parser.parse_args()


if __name__ == '__main__':
    main()
