__author__ = 'ict'

import os

from bs_grammmar_analysis import bs_token_list, bs_grammar_analyzer
from bs_slr_generate import bs_slr_generate_table
from bs_lr_generate import bs_lr_generate_table
from boson.bs_code_generate import *

code_generator = {
    "python": bs_generate_python_code
}

grammar_generate_table = {
    "slr": bs_slr_generate_table,
    "lr":  bs_lr_generate_table,
}


def usage():
    print("======== %s ========" % boson_title)
    print("Author: " + boson_author)
    print("Email: " + boson_author_email)
    print()
    print("Usage:")
    print("    " + sys.argv[0] + " [grammar file] -o/output <code file> -a/analyzer <analyzer> -l/language <language>")


def main(argv):
    if len(argv) < 2:
        usage()
        exit()
    grammar_file = sys.argv[1]
    code_file = None
    analyzer = "slr"
    language = "python"
    i = 2
    while i < len(argv):
        if argv[i][0] == "-":
            option = argv[i][1:]
            i += 1
            if option == "o" or option == "output":
                if i < len(argv):
                    code_file = argv[i]
                else:
                    usage()
                    exit()
            elif option == "a" or option == "analyzer":
                if i < len(argv) - 1:
                    analyzer = argv[i].lower()
                else:
                    usage()
                    exit()
            elif option == "l" or option == "language":
                if i < len(argv) - 1:
                    language = argv[i].lower()
                else:
                    usage()
                    exit()
            else:
                usage()
                exit()
            i += 1
        else:
            usage()
            exit()
    if analyzer not in grammar_generate_table:
        usage()
        print("Analyzer: " + ", ".join(list(grammar_generate_table)))
        exit()
    if language not in code_generator:
        usage()
        print("Language: " + ", ".join(list(code_generator)))
        exit()
    if code_file is not None:
        fp = open(code_file, "w")
    else:
        fp = sys.stdout
    try:
        print("Parse grammar file...", end="")
        sentence_set = bs_grammar_analyzer(bs_token_list(grammar_file))
        print("Done")
        print("Generate %s grammar analysis table..." % analyzer.upper(), end="")
        analyzer_table = grammar_generate_table[analyzer](sentence_set)
        print("Done")
        print("Generate analyzer %s code..." % language.upper(), end="")
        code_generator[language](analyzer_table, fp)
        print("Done")
        if code_file is not None:
            fp.close()
    except Exception as e:
        print(e)
        fp.close()
        os.remove(code_file)

if __name__ == "__main__":
    main(sys.argv)