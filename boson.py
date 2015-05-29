__author__ = 'ict'

import os
import argparse
import time
from argparse import RawTextHelpFormatter

from boson.bs_grammar_analysis import bs_grammar_analysis
from boson.bs_lexcial_analyzer import BosonLexicalAnalyzer
from boson.bs_slr_generate import bs_slr_generate_table
from boson.bs_lr_generate import bs_lr_generate_table
from boson.bs_lalr_generate import bs_lalr_generate_table
from boson.bs_code_generate import *

code_generator = {
    "python3": bs_generate_python_code
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
    lex_file = argv.lexical
    analyzer = argv.analyzer
    language = argv.code
    lex = None
    if code_file is not None:
        fp = open(code_file, "w")
    else:
        fp = sys.stdout
    try:
        print("Parse grammar file...", end="")
        start_time = time.time()
        global_start_time = start_time
        data_package = bs_grammar_analysis(grammar_file)
        sentence_set = data_package["sentence set"]
        end_time = time.time()
        print("Done [%fs]" % ((end_time - start_time) / 1000))
        if lex_file is not None:
            print("Parse lexical file...", end="")
            start_time = time.time()
            lex = BosonLexicalAnalyzer(lex_file)
            print("Done [%fs]" % ((end_time - start_time) / 1000))
        print("Generate %s grammar analysis table..." % analyzer.upper(), end="")
        start_time = time.time()
        analyzer_table = grammar_generate_table[analyzer](sentence_set)
        end_time = time.time()
        print("Done [%fs]" % ((end_time - start_time) / 1000))
        print("Generate analyzer %s code..." % language.upper(), end="")
        start_time = time.time()
        code_generator[language](analyzer_table, data_package, lex=lex, output=fp)
        end_time = time.time()
        print("Done [%fs]" % ((end_time - start_time) / 1000))
        if code_file is not None:
            fp.close()
        global_end_time = time.time()
        print("Complete!!! [%fs]" % ((global_end_time - global_start_time) / 1000))
    except Exception as e:
        print(e)
        if code_file is not None:
            fp.close()
            if os.path.exists(code_file):
                os.remove(code_file)

if __name__ == "__main__":
    parse = argparse.ArgumentParser(description="%s commandline" % boson_title, formatter_class=RawTextHelpFormatter)
    parse.add_argument("grammar_file", help="Inpute grammar description file.")
    parse.add_argument("-o", "--output", help="Output grammar analyzer code.")
    parse.add_argument("-l", "--lexical", help="Lexical analysis file.")
    parse.add_argument("-a", "--analyzer", default="slr", choices=["slr", "lr", "lalr"],
                       help="Analyzer type (default is SLR).\n"
                            "slr  - SLR(Simple LR)\n"
                            "lr   - LR(Canonical LR)\n"
                            "lalr - LALR(Look-Ahead LR)\n"
                       )
    parse.add_argument("-c", "--code", default="python3", choices=["python3"],
                       help="Generate code language (default is Python3).\n"
                            "python3 - Python3 code.\n"
                       )
    args = parse.parse_args()
    main(args)
