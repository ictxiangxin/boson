__author__ = 'ict'

import os
import argparse
import time
from argparse import RawTextHelpFormatter

from boson.bs_grammmar_analysis import bs_token_list, bs_grammar_analyzer
from boson.bs_slr_generate import bs_slr_generate_table
from boson.bs_lr_generate import bs_lr_generate_table
from boson.bs_lalr_generate import bs_lalr_generate_table
from boson.bs_code_generate import *

code_generator = {
    "python": bs_generate_python_code
}

grammar_generate_table = {
    "slr":  bs_slr_generate_table,
    "lr":   bs_lr_generate_table,
    "lalr": bs_lalr_generate_table,
}


def welcome():
    print("======== %s ========" % boson_title)
    print("Author: " + boson_author)
    print("Email: " + boson_author_email)
    print()


def main(argv):
    welcome()
    grammar_file = argv.grammar_file
    code_file = argv.output
    analyzer = argv.analyzer
    language = argv.language
    if code_file is not None:
        fp = open(code_file, "w")
    else:
        fp = sys.stdout
    try:
        print("Parse grammar file...", end="")
        start_time = time.time()
        global_start_time = start_time
        sentence_set, reduce_code = bs_grammar_analyzer(bs_token_list(grammar_file))
        end_time = time.time()
        print("Done [%fs]" % ((end_time - start_time) / 1000))
        print("Generate %s grammar analysis table..." % analyzer.upper(), end="")
        start_time = time.time()
        analyzer_table = grammar_generate_table[analyzer](sentence_set)
        end_time = time.time()
        print("Done [%fs]" % ((end_time - start_time) / 1000))
        print("Generate analyzer %s code..." % language.upper(), end="")
        start_time = time.time()
        code_generator[language](analyzer_table, reduce_code, fp)
        end_time = time.time()
        global_end_time = time.time()
        print("Done [%fs]" % ((end_time - start_time) / 1000))
        print("Complete!!! [%fs]" % ((global_end_time - global_start_time) / 1000))
        if code_file is not None:
            fp.close()
    except Exception as e:
        print(e)
        fp.close()
        os.remove(code_file)

if __name__ == "__main__":
    parse = argparse.ArgumentParser(description="%s commandline" % boson_title, formatter_class=RawTextHelpFormatter)
    parse.add_argument("grammar_file", help="Inpute grammar description file.")
    parse.add_argument("-o", "--output", help="Output grammar analyzer code.")
    parse.add_argument("-a", "--analyzer", default="slr", choices=["slr", "lr", "lalr"],
                       help="Analyzer type (default is SLR).\n"
                            "slr  - SLR(Simple LR)\n"
                            "lr   - LR(Canonical LR)\n"
                            "lalr - LALR(Look-Ahead LR)\n"
                       )
    parse.add_argument("-l", "--language", default="python", choices=["python3"],
                       help="Generate code language (default is Python3).\n"
                            "python3 - Python3 code.\n"
                       )
    args = parse.parse_args()
    main(args)
