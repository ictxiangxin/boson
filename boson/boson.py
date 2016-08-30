import os
import sys
import argparse
import time
from argparse import RawTextHelpFormatter
import boson.bs_configure as configure
from boson.bs_command import bs_command_execute
from boson.bs_grammar_analysis import bs_grammar_analysis
from boson.bs_slr_generate import bs_slr_generate_table
from boson.bs_lr_generate import bs_lr_generate_table
from boson.bs_lalr_generate import bs_lalr_generate_table
from boson.bs_code_generator import bs_generate_code

grammar_generate_table = {
    "slr":  bs_slr_generate_table,
    "lr":   bs_lr_generate_table,
    "lalr": bs_lalr_generate_table,
}


def welcome():
    print("%s - %s" % (configure.boson_title, configure.boson_description), flush=True)
    print("    Author: %s" % configure.boson_author, flush=True)
    print("    Email:  %s" % configure.boson_author_email, flush=True)
    print(flush=True)


def boson_main():
    parse = argparse.ArgumentParser(description="%s - %s" % (configure.boson_title, configure.boson_description),
                                    formatter_class=RawTextHelpFormatter)
    parse.add_argument("grammar_file",
                       help="Inpute grammar description file.")
    parse.add_argument("-t", "--type", default="bnf", choices=["bnf", "ebnf"],
                       help="Input file type (default is BNF).\n"
                            "  bnf  - BNF grammar file, can define special grammar tuple.\n"
                            "  ebnf - EBNF grammar file, can not define special grammar tuple.\n")
    parse.add_argument("-o", "--output",
                       help="Output grammar analyzer code.")
    parse.add_argument("-a", "--analyzer", default="lalr", choices=["slr", "lr", "lalr"],
                       help="Analyzer type (default is LALR).\n"
                            "  slr  - SLR (Simple LR)\n"
                            "  lr   - LR (Canonical LR)\n"
                            "  lalr - LALR (Look-Ahead LR)\n")
    parse.add_argument("-c", "--code", default="python3", choices=["python3"],
                       help="Generate code language (default is Python3).\n"
                            "  python3 - Python3 code.\n")
    parse.add_argument("-r", "--report", action="store_true",
                       help="Report conflict when create grammar analyzer.")
    parse.add_argument("-f", "--force", action="store_true",
                       help="Force generate code when exist conflict.")
    arguments = parse.parse_args()
    welcome()
    fp = None
    try:
        if arguments.type == "bnf":
            print("[Generate grammar analyzer code]", flush=True)
            print("    Parse grammar file...", end="", flush=True)
            start_time = time.time()
            global_start_time = start_time
            grammar_package = bs_grammar_analysis(arguments.grammar_file)
            bs_command_execute(grammar_package.command_list)
            end_time = time.time()
            print("Done [%fs]" % (end_time - start_time), flush=True)
            print("    Generate %s grammar analysis table..." % arguments.analyzer.upper(), end="", flush=True)
            start_time = time.time()
            analyzer_table = grammar_generate_table[arguments.analyzer](grammar_package.sentence_set)
            end_time = time.time()
            print("Done [%fs]" % (end_time - start_time), flush=True)
            if arguments.report and len(analyzer_table.conflict_list):
                conflict_type_text = {
                    configure.boson_conflict_reduce_reduce: "Reduce/Reduce",
                    configure.boson_conflict_shift_reduce: "Shift/Reduce"
                }
                print("[Conflict information]", flush=True)
                for state_number, confict_type, terminal in analyzer_table.conflict_list:
                    print("    [Conflict state: %d] %s Terminal: %s" % (state_number, conflict_type_text[confict_type], terminal), flush=True)
                if not arguments.force:
                    return
            print("    Generate analyzer %s code..." % arguments.code.upper(), end="", flush=True)
            start_time = time.time()
            if arguments.output is not None:
                fp = open(arguments.output, "w")
                end_string = ""
            else:
                fp = sys.stdout
                end_string = "\n\n"
            text = bs_generate_code(arguments.code, analyzer_table, grammar_package)
            fp.write(text)
            end_time = time.time()
            print(end_string + "Done [%fs]" % (end_time - start_time), flush=True)
            if arguments.output is not None:
                fp.close()
            global_end_time = time.time()
            print("    Complete!!! [%fs]" % (global_end_time - global_start_time))
        elif arguments.type == "ebnf":
            print("Not support now")
        else:
            raise Exception("Invalid file type: %s" % arguments.type)
    except Exception as e:
        print("\n%s" % str(e), file=sys.stderr, flush=True)
        if arguments.output is not None:
            if fp is not None:
                fp.close()
            if os.path.exists(arguments.output):
                os.remove(arguments.output)
