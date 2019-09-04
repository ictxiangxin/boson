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
    'slr': bs_slr_generate_table,
    'lr': bs_lr_generate_table,
    'lalr': bs_lalr_generate_table,
}


def display(text, newline=True, file=sys.stdout):
    print(text, end=('\n' if newline else ''), flush=True, file=file)


def welcome():
    display('{} - {}'.format(configure.boson_title, configure.boson_description))
    display('    Author: {}'.format(configure.boson_author))
    display('    Email:  {}'.format(configure.boson_email))
    display('    Site:   {}'.format(configure.boson_url))
    display('')


def console_main():
    parse = argparse.ArgumentParser(description='{} - {}'.format(configure.boson_title, configure.boson_description),
                                    formatter_class=RawTextHelpFormatter)
    parse.add_argument('grammar_file',
                       help='Inpute grammar description file.')
    parse.add_argument('-o', '--output',
                       help='Output grammar analyzer code.')
    parse.add_argument('-a', '--analyzer', default='lalr', choices=['slr', 'lr', 'lalr'],
                       help='Analyzer type (default is LALR).\n'
                            '  slr  - SLR (Simple LR)\n'
                            '  lr   - LR (Canonical LR)\n'
                            '  lalr - LALR (Look-Ahead LR)\n')
    parse.add_argument('-l', '--language', default='python3', choices=['python3', 'c++'],
                       help='Generate code language (default is Python3).\n'
                            '  python3 - Python3 code.\n'
                            '  c++ - C++ code.\n')
    parse.add_argument('-f', '--force', action='store_true',
                       help='Force generate code when exist conflict.')
    parse.add_argument('-q', '--quiet', action='store_true',
                       help='Do not output code when executing boson script.')
    arguments = parse.parse_args()
    welcome()
    source_file = None
    output_file = None
    output_file_exist = False
    try:
        if arguments.output is not None and os.path.exists(arguments.output):
            output_file_exist = True
        display('[Generate grammar analyzer code]')
        display('    Parse grammar file... ', newline=False)
        start_time = time.time()
        global_start_time = start_time
        source_file = open(arguments.grammar_file, 'r', encoding='utf-8')
        grammar_package = bs_grammar_analysis(source_file.read())
        bs_command_execute(grammar_package.command_list)
        end_time = time.time()
        display('Done [{:.4f}s]'.format(end_time - start_time))
        display('    Generate {} grammar analysis table... '.format(arguments.analyzer.upper()), newline=False)
        start_time = time.time()
        analyzer_table = grammar_generate_table[arguments.analyzer](grammar_package.sentence_set)
        end_time = time.time()
        display('Done [{:.4f}s]'.format(end_time - start_time))
        if len(analyzer_table.conflict_list):
            conflict_type_text = {
                configure.boson_conflict_reduce_reduce: 'Reduce/Reduce',
                configure.boson_conflict_shift_reduce: 'Shift/Reduce'
            }
            display('[Error] Conflict')
            for state_number, conflict_type, terminal in analyzer_table.conflict_list:
                if terminal in grammar_package.literal_reverse_map:
                    terminal = '\'{}\''.format(grammar_package.literal_reverse_map[terminal])
                display('    [Conflict state: {}] {} Terminal: {}'.format(state_number, conflict_type_text[conflict_type], terminal))
        if not arguments.force and len(analyzer_table.conflict_list):
            return
        if arguments.output is not None:
            output_file = open(arguments.output, 'w', encoding='utf-8')
        elif arguments.quiet:
            output_file = None
        else:
            output_file = sys.stdout
        display('    Generate analyzer {} code... '.format(arguments.language.upper()), newline=False)
        start_time = time.time()
        text = bs_generate_code(arguments.language, analyzer_table, grammar_package)
        end_time = time.time()
        display('Done [{:.4f}s]'.format(end_time - start_time))
        global_end_time = time.time()
        display('    Complete!!! [{:.4f}s]'.format(global_end_time - global_start_time))
        display('')
        if output_file is not None:
            output_file.write(text)
    except Exception as e:
        display('\n\n[Error] {}'.format(e), file=sys.stderr)
        if arguments.output is not None and output_file is not None:
            output_file.close()
            if os.path.exists(arguments.output) or not output_file_exist:
                os.remove(arguments.output)
    finally:
        if source_file is not None:
            source_file.close()
        if arguments.output is not None and output_file is not None:
            output_file.close()
