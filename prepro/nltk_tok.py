#!/usr/bin/python

import sys
import argparse
import nltk
import os
import multiprocessing

NLTK_DATA = "{}/.local/share/nltk_data".format(os.path.expanduser("~"))
THREADS = 16
SEGMENTER = None
NORMALIZE_QUOTES = False
CHUNKSIZE = 16


def main():
    args = parse_args()
    nltk.data.path.append(args.nltk_data)

    global NORMALIZE_QUOTES, SEGMENTER
    NORMALIZE_QUOTES = args.change_quotes

    if args.split_lines:
        SEGMENTER = nltk.data.load("tokenizers/punkt/{}.pickle".format(
            args.language))
        func = nltk_segmentize
    else:
        func = nltk_tokenize

    for line in sys.stdin:
        line = line.decode("UTF-8")
        print func(line).encode("UTF-8")
    #pool = multiprocessing.Pool(args.jobs)
    #for result in pool.imap(func, sys.stdin, chunksize=CHUNKSIZE):
    #    print result
    #pool.close()
    #pool.join()


def nltk_segmentize(line):
    sents = []
    line = line.decode("utf-8")
    for sent in SEGMENTER.tokenize(line.lstrip()):
        sents.append(nltk_tokenize(sent))
    return "\n".join(sents)


def nltk_tokenize(line):
    toks = " ".join(nltk.word_tokenize(line.strip()))
    if not NORMALIZE_QUOTES:
        toks = toks.replace("``", '"').replace("''", '"')
    return toks


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-l",
        "--language",
        help="language, default: english",
        default="english")
    parser.add_argument(
        "-q",
        "--change-quotes",
        help="replace \"*\" with ``*''",
        action="store_true")
    parser.add_argument(
        "-s",
        "--split-lines",
        help="more than one sentence per line is possible",
        action="store_true")
    parser.add_argument(
        "--nltk-data", help="path to NLTK data", default=NLTK_DATA)
    parser.add_argument(
        "-j",
        "--jobs",
        help="number of parallel jobs, default: 16",
        type=int,
        default=THREADS)
    return parser.parse_args()


if __name__ == "__main__":
    main()
