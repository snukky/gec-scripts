#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import argparse
import re
import difflib
import collections

MIN_CHARS = 3
COUNT_LOG = 10000


def main():
    args = parse_user_args()

    patterns = collections.defaultdict(int)
    for i, line in enumerate(args.input):
        err_sent, cor_sent = line.strip().split('\t')[:2]

        for err, cor in iterate_edits(err_sent.split(), cor_sent.split()):
            pattern, string = make_pattern(err, cor)
            patterns['{}\t{}'.format(pattern, string)] += 1

            if args.edits:
                args.edits.write('{}\t{}\n'.format(err, cor))

        if (i + 1) % COUNT_LOG == 0:
            print >>sys.stderr, "[{}]".format(i + 1)

    for p in sorted(patterns, key=patterns.get, reverse=True):
        args.output.write('{}\t{}\n'.format(p, patterns[p]))


def make_pattern(a, b):
    pattern = ''
    string = ''

    if a == b:
        pattern = '^' + re.escape(a) + '$'
        string = a
    elif not a and b:
        pattern = '^' + re.escape("NULL -> {}".format(b)) + '$'
        string = "ins(«{}»)".format(re.sub(r'\s', r'·', b))
    elif a and not b:
        pattern = '^' + re.escape("{} -> NULL".format(a)) + '$'
        string = "del(«{}»)".format(re.sub(r'\s', r'·', a))
    else:
        matcher = difflib.SequenceMatcher(None, a, b)

        left_pattern = ''
        right_pattern = ''
        left_string = ''
        right_string = ''
        same_idx = 0

        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            a_str = a[i1:i2]
            b_str = b[j1:j2]

            if tag == 'equal' and len(a_str) > MIN_CHARS:
                same_idx += 1
                left_pattern += '(\w{3,})'
                left_string += '(\w{3,})'
                right_pattern += '\\{}'.format(same_idx)
                right_string += '\\{}'.format(same_idx)
                continue

            left_pattern += re.escape(a_str)
            left_string += a_str
            right_pattern += re.escape(b_str)
            right_string += b_str

        pattern = '^' + left_pattern + re.escape(' -> ') + right_pattern + '$'
        string = 'sub(«{}»,«{}»)'.format(left_string, right_string)
        string = re.sub(r'\s', r'·', string)

    return pattern, string


def iterate_edits(err_toks, cor_toks):
    matcher = difflib.SequenceMatcher(None, err_toks, cor_toks)

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'replace':
            err_tok = ' '.join(err_toks[i1:i2])
            cor_tok = ' '.join(cor_toks[j1:j2])
            yield err_tok, cor_tok
        elif tag == 'insert':
            cor_tok = ' '.join(cor_toks[j1:j2])
            yield '', cor_tok
        elif tag == 'delete':
            err_tok = ' '.join(err_toks[i1:i2])
            yield err_tok, ''


def parse_user_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', nargs='?', type=argparse.FileType('r'),
                        default=sys.stdin, help="input parallel sentences")
    parser.add_argument('output', nargs='?', type=argparse.FileType('w'),
                        default=sys.stdout, help="output patterns")
    parser.add_argument('-e', '--edits', metavar='FILE', nargs='?',
                        type=argparse.FileType('w'),
                        help="write edits into file")
    return parser.parse_args()


if __name__ == '__main__':
    main()
