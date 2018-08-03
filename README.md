# GEC Scripts

A set of scripts for processing data for grammatical error correction.


### Edits

* `edits/extract_edits.py` - extract edits from parallel sentences
* `edits/calculate_stats.py` - calculate edit statistics like error rates and a number of substitutions, deletions, insertions
* `edits/reduce_error_rate.py` - remove correct sentences to get desired sentence error rate

Examples:

    python extract_edits.py -d ' => ' < file.txt > edits.txt

### Error patterns

* `patterns/extract_patterns.py` - extract regex patterns from parallel sentences
* `patterns/filter_patterns.py` - filter out edits that do not match referential patterns

Examples:

    python extract_patterns.py < file.txt > patterns.txt
    python filter_patterns.py -p patterns.txt -m 3 < corpus.txt > filtered.txt

### Tokenization

* `nltk/nltk_tok.py` - a wrapper for the NLTK tokenizer
* `nltk/nltk_detok.py` - a NLTK-compatible detokenizer

Examples:

    python nltk_tok.py -q -j8 < file.txt > file.tok.txt
    python nltk_detok.py < file.tok.txt > file.txt

