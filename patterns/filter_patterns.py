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

    patterns = load_patterns(args.patterns, args.min_freq)

    for i, line in enumerate(args.input):
        err_sent, cor_sent = line.strip().split('\t')[:2]

        err_toks = err_sent.split()
        cor_toks = cor_sent.split()
        new_toks = []
        matcher = difflib.SequenceMatcher(None, err_toks, cor_toks)

        if args.debug:
            debug( "ERR: {}".format(err_sent))
            debug( "COR: {}".format(cor_sent))

        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            err_tok = ' '.join(err_toks[i1:i2])
            cor_tok = ' '.join(cor_toks[j1:j2])

            if tag == 'equal':
                new_toks.append(err_tok)
            else:
                edit, _ = make_pattern(err_tok, cor_tok)
                match = edit in patterns
                if args.correction:
                    new_toks.append(cor_tok if match else err_tok)
                else:
                    new_toks.append(err_tok if match else cor_tok)

                if args.debug:
                    debug("match: {}".format(match))
                    debug("{}\t\t{} -> {}".format(new_toks, err_tok, cor_tok))

                # found = False
                # for regex in regexes:
                    # if re.match(regex, edit):
                    # new_toks.append(err_tok)
                    # found = True
                    # break
                # if not found:
                    # new_toks.append(cor_tok)

        new_sent = re.sub(r'\s+', ' ', ' '.join(new_toks)).strip()
        if args.correction:
            args.output.write('{}\t{}\n'.format(err_sent, new_sent))
        else:
            args.output.write('{}\t{}\n'.format(new_sent, cor_sent))

        if (i + 1) % COUNT_LOG == 0:
            debug("[{}]".format(i + 1))


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


def load_patterns(pattern_io, min_freq=5):
    debug("min. frequency: {}".format(min_freq))
    patterns = []
    count_all = 0
    count_used = 0
    num = 0
    for i, line in enumerate(pattern_io):
        pattern, _, sfreq = line.strip().split("\t")
        freq = int(sfreq)
        if freq >= min_freq:
            patterns.append(pattern)
            count_used += freq
        count_all += freq
        num += 1
    # return re.compile('|'.join(patterns))
    # return [re.compile(patt) for patt in patterns]
    debug("{}/{} patterns loaded".format(len(patterns), num))
    frac = count_used / float(count_all)
    debug("loaded patterns cover {:.4f} cases".format(frac))
    return set(patterns)


def debug(msg):
    print >>sys.stderr, msg


def parse_user_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', nargs='?', type=argparse.FileType('r'),
                        default=sys.stdin, help="input parallel sentences")
    parser.add_argument('output', nargs='?', type=argparse.FileType('w'),
                        default=sys.stdout, help="output parallel sentences")
    parser.add_argument('-p', '--patterns', type=argparse.FileType('r'),
                        required=True, help="patterns")
    parser.add_argument('-m', '--min-freq', type=int, default=5,
                        help="minimum pattern frequency")
    parser.add_argument('-c', '--correction', action='store_true',
                        help="do correction")
    parser.add_argument('--debug', action='store_true', help='show debugs')
    return parser.parse_args()


if __name__ == '__main__':
    main()
