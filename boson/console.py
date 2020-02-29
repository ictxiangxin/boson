import os
import sys
import argparse
import time
from argparse import RawTextHelpFormatter
import boson.configure as configure
from boson.boson_script import CommandExecutor
from boson.lexer_generator import LexerGenerator
from boson.boson_script import BosonScriptAnalyzer
from boson.parser_generator import \
    BottomUpParserGenerator, \
    BottomUpCanonicalParserGenerator, \
    SLRParserGenerator, \
    LRParserGenerator, \
    LALRParserGenerator
from boson.code_generator import CodeGenerator

parser_generator_library = {
    'slr': SLRParserGenerator,
    'lr': LRParserGenerator,
    'lalr': LALRParserGenerator,
}

quiet = False


def display(text: str, newline: bool = True, file=sys.stdout):
    if not quiet:
        print(text, end=('\n' if newline else ''), flush=True, file=file)


def welcome():
    display('{} - {}'.format(configure.boson_title, configure.boson_description))
    display('    Author: {}'.format(configure.boson_author))
    display('    Email:  {}'.format(configure.boson_email))
    display('    URL:    {}'.format(configure.boson_url))
    display('')


def console_main():
    parse = argparse.ArgumentParser(description='{} - {}'.format(configure.boson_title, configure.boson_description),
                                    formatter_class=RawTextHelpFormatter)
    parse.add_argument('boson_script_file',
                       help='Input Boson Script File.')
    parse.add_argument('-o', '--output',
                       help='Output Lexer&Parser Code File.')
    parse.add_argument('-a', '--analyzer', default='lalr', choices=['slr', 'lr', 'lalr'],
                       help='Grammar Analyzer Type (Default Is LALR).\n'
                            '  slr  - SLR(1) (Simple LR)\n'
                            '  lr   - LR(1) (Canonical LR)\n'
                            '  lalr - LALR(1) (Look-Ahead LR)\n')
    parse.add_argument('-l', '--language', default='python3', choices=['python3', 'c++'],
                       help='Generate Code Program Language (Default Is Python3).\n'
                            '  python3 - Python3 Code.\n'
                            '  c++ - C++ Code.\n')
    parse.add_argument('-f', '--force', action='store_true',
                       help='Force Generate Parse Table When Exist Conflicts.')
    parse.add_argument('-q', '--quiet', action='store_true',
                       help='Display Nothing.')
    arguments = parse.parse_args()
    global quiet
    quiet = arguments.quiet
    welcome()
    source_file = None
    output_file = None
    output_file_exist = False
    try:
        if arguments.output is not None and os.path.exists(arguments.output):
            output_file_exist = True
        display('[Generate Analyzer Code]')
        step = 1
        display('    [{}] Parse Boson Script... '.format(step), newline=False)
        start_time = time.time()
        global_start_time = start_time
        source_file = open(arguments.boson_script_file, 'r', encoding=configure.boson_default_encoding)
        script_analyzer = BosonScriptAnalyzer()
        script_analyzer.tokenize_and_parse(source_file.read())
        command_executor = CommandExecutor()
        command_executor.execute(script_analyzer.command_list())
        end_time = time.time()
        display('Done [{:.4f}s]'.format(end_time - start_time))
        display('        > Commands Count: {}'.format(len(script_analyzer.command_list())))
        display('        > Lexical Definition: {}'.format('Yes' if script_analyzer.lexical_definition() else 'No'))
        display('        > Grammar Definition: {}'.format('Yes' if script_analyzer.sentence_set() else 'No'))
        if configure.boson_option['generate_lexer'] == 'yes' and script_analyzer.lexical_definition():
            step += 1
            display('    [{}] Generate Lexical Analysis Table... '.format(step), newline=False)
            start_time = time.time()
            lexical_analyzer = LexerGenerator(script_analyzer.lexical_definition())
            lexical_analyzer.generate_lexical_dfa()
            lexical_analyzer.generate_compact_move_table()
            end_time = time.time()
            display('Done [{:.4f}s]'.format(end_time - start_time))
            display('        > Lexical Definition Count: {}'.format(len(script_analyzer.lexical_definition())))
            display('        > Character Set Size: {}'.format(len(lexical_analyzer.character_set())))
            display('        > DFA State Count: {}'.format(len(lexical_analyzer.compact_move_table())))
        else:
            lexical_analyzer = None
        if script_analyzer.sentence_set():
            step += 1
            display('    [{}] Generate Grammar Analysis Table... '.format(step), newline=False)
            start_time = time.time()
            parser_generator = parser_generator_library[arguments.analyzer](script_analyzer.sentence_set())
            parser_generator.initialize()
            parser_generator.assemble_sentence_grammar_name(script_analyzer.sentence_grammar_name_mapping())
            parser_generator.assemble_naive_sentence(script_analyzer.naive_sentence_set())
            parser_generator.assemble_grammar_tuple(script_analyzer.sentence_grammar_tuple_mapping())
            parser_generator.generate_parser_dfa()
            parser_generator.generate_parse_table()
            parser_generator.parse_table_sparsification()
            end_time = time.time()
            display('Done [{:.4f}s]'.format(end_time - start_time))
            display('        > Algorithm: {}'.format(arguments.analyzer.upper()))
            display('        > Grammar Sentence Count: {}'.format(len(parser_generator.origin_sentence_list())))
            display('        > Non-Terminal Symbol Count: {}'.format(len(parser_generator.non_terminal_set())))
            display('        > Terminal Symbol Count: {}'.format(len(parser_generator.terminal_set())))
            if isinstance(parser_generator, BottomUpParserGenerator):
                display('        > PDA State Count: {}'.format(len(parser_generator.state_reduce_mapping())))
                if isinstance(parser_generator, BottomUpCanonicalParserGenerator):
                    action_table_size = sum([len(line) for line in parser_generator.action_table()])
                    sparse_action_table_size = sum([len(line) for _, line in parser_generator.sparse_action_table().items()])
                    action_table_compression_rate = sparse_action_table_size / action_table_size * 100 if action_table_size > 0 else 0
                    goto_table_size = sum([len(line) for line in parser_generator.goto_table()])
                    sparse_goto_table_size = sum([len(line) for _, line in parser_generator.sparse_goto_table().items()])
                    goto_table_compression_rate = sparse_goto_table_size / goto_table_size * 100 if goto_table_size > 0 else 0
                    display('        > Action Table Size/Sparse-Size (Rate): {}/{} ({:.2f}%)'.format(action_table_size, sparse_action_table_size, action_table_compression_rate))
                    display('        > Goto Table Size/Sparse-Size (Rate): {}/{} ({:.2f}%)'.format(goto_table_size, sparse_goto_table_size, goto_table_compression_rate))
            if parser_generator.conflict_list():
                conflict_type_text = {
                    configure.boson_conflict_reduce_reduce: 'Reduce/Reduce',
                    configure.boson_conflict_shift_reduce: 'Shift/Reduce'
                }
                display('    [Error] Conflict')
                for state_number, conflict_type, terminal in parser_generator.conflict_list():
                    if terminal in script_analyzer.literal_reverse_map():
                        terminal = '\'{}\''.format(script_analyzer.literal_reverse_map()[terminal])
                    display('        [Conflict state: {}] {} Terminal: {}'.format(state_number, conflict_type_text[conflict_type], terminal))
            if not arguments.force and parser_generator.conflict_list():
                return
        else:
            parser_generator = None
        if arguments.output is not None:
            output_file = open(arguments.output, 'w', encoding=configure.boson_default_encoding)
        elif quiet:
            output_file = None
        else:
            output_file = sys.stdout
        step += 1
        display('    [{}] Generate Code... '.format(step), newline=False)
        start_time = time.time()
        code_generator = CodeGenerator(arguments.language)
        if lexical_analyzer is not None:
            code_generator.dispose_lexer(lexical_analyzer)
        if parser_generator is not None:
            code_generator.dispose_parser(parser_generator)
        code_text = code_generator.generate_code()
        end_time = time.time()
        display('Done [{:.4f}s]'.format(end_time - start_time))
        display('        > Language: {}'.format(arguments.language.upper()))
        display('        > Generate Lexer: {}'.format('Yes' if lexical_analyzer else 'No'))
        display('        > Generate Parser: {}'.format('Yes' if parser_generator else 'No'))
        global_end_time = time.time()
        display('[Complete!!! {:.4f}s]'.format(global_end_time - global_start_time))
        display('')
        if output_file is not None:
            output_file.write(code_text)
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
