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
    'slr':  bs_slr_generate_table,
    'lr':   bs_lr_generate_table,
    'lalr': bs_lalr_generate_table,
}


def welcome():
    print('{} - {}'.format(configure.boson_title, configure.boson_description), flush=True)
    print('    Author: {}'.format(configure.boson_author), flush=True)
    print('    Email:  {}'.format(configure.boson_email), flush=True)
    print('    Site:   {}'.format(configure.boson_url), flush=True)
    print(flush=True)


def console_main():
    parse = argparse.ArgumentParser(description='{} - {}'.format(configure.boson_title, configure.boson_description),
                                    formatter_class=RawTextHelpFormatter)
    parse.add_argument('grammar_file',
                       help='Inpute grammar description file.')
    parse.add_argument('-t', '--type', default='bnf', choices=['bnf', 'ebnf'],
                       help='Input file type (default is BNF).\n'
                            '  bnf  - BNF grammar file, can define special grammar tuple.\n'
                            '  ebnf - EBNF grammar file, can not define special grammar tuple.\n')
    parse.add_argument('-o', '--output',
                       help='Output grammar analyzer code.')
    parse.add_argument('-a', '--analyzer', default='lalr', choices=['slr', 'lr', 'lalr'],
                       help='Analyzer type (default is LALR).\n'
                            '  slr  - SLR (Simple LR)\n'
                            '  lr   - LR (Canonical LR)\n'
                            '  lalr - LALR (Look-Ahead LR)\n')
    parse.add_argument('-c', '--code', default='python3', choices=['python3'],
                       help='Generate code language (default is Python3).\n'
                            '  python3 - Python3 code.\n')
    parse.add_argument('-r', '--report', action='store_true',
                       help='Report conflict when create grammar analyzer.')
    parse.add_argument('-f', '--force', action='store_true',
                       help='Force generate code when exist conflict.')
    parse.add_argument('-s', '--sparse', action='store_true',
                       help='Use sparse analyzer tables.')
    arguments = parse.parse_args()
    welcome()
    source_file = None
    output_file = None
    output_file_exist = False
    try:
        if arguments.output is not None and os.path.exists(arguments.output):
            output_file_exist = True
        if arguments.type == 'bnf':
            print('[Generate grammar analyzer code]', flush=True)
            print('    Parse grammar file... ', end='', flush=True)
            start_time = time.time()
            global_start_time = start_time
            source_file = open(arguments.grammar_file, 'r', encoding='utf-8')
            grammar_package = bs_grammar_analysis(source_file.read())
            bs_command_execute(grammar_package.command_list)
            end_time = time.time()
            print('Done [{:.4f}s]'.format(end_time - start_time), flush=True)
            print('    Generate {} grammar analysis table... '.format(arguments.analyzer.upper()), end='', flush=True)
            start_time = time.time()
            analyzer_table = grammar_generate_table[arguments.analyzer](grammar_package.sentence_set)
            end_time = time.time()
            print('Done [{:.4f}s]'.format(end_time - start_time), flush=True)
            if arguments.report and len(analyzer_table.conflict_list):
                conflict_type_text = {
                    configure.boson_conflict_reduce_reduce: 'Reduce/Reduce',
                    configure.boson_conflict_shift_reduce: 'Shift/Reduce'
                }
                print('[Conflict information]', flush=True)
                for state_number, confict_type, terminal in analyzer_table.conflict_list:
                    print('    [Conflict state: {}] {} Terminal: {}'.format(state_number, conflict_type_text[confict_type], terminal), flush=True)
                if not arguments.force:
                    return
            if arguments.output is not None:
                output_file = open(arguments.output, 'w', encoding='utf-8')
            else:
                output_file = sys.stdout
            print('    Generate analyzer {} code... '.format(arguments.code.upper()), end='', flush=True)
            start_time = time.time()
            text = bs_generate_code(arguments.code, analyzer_table, grammar_package, arguments.sparse)
            end_time = time.time()
            print('Done [{:.4f}s]'.format(end_time - start_time), flush=True)
            global_end_time = time.time()
            print('    Complete!!! [{:.4f}s]\n'.format(global_end_time - global_start_time))
            output_file.write(text)
        elif arguments.type == 'ebnf':
            print('Not support now')
        else:
            raise Exception('Invalid file type: {}'.format(arguments.type))
    except Exception as e:
        print('\n\n[Error] {}'.format(e), file=sys.stderr, flush=True)
        if arguments.output is not None and output_file is not None:
            output_file.close()
            if os.path.exists(arguments.output) or not output_file_exist:
                os.remove(arguments.output)
    finally:
        if source_file is not None:
            source_file.close()
        if arguments.output is not None and output_file is not None:
            output_file.close()
