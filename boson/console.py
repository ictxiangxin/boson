import argparse
import os
import sys
import time
import traceback
from argparse import RawTextHelpFormatter

import boson.configure as configure
from boson.option import option as boson_option
from boson.boson_script import BosonScriptAnalyzer
from boson.boson_script import CommandExecutor
from boson.code_generator import \
    PythonCodeGenerator, \
    CppCodeGenerator, \
    JavaCodeGenerator, \
    JavaScriptCodeGenerator
from boson.lexer_generator import LexerGenerator
from boson.parser_generator import \
    BottomUpParserGenerator, \
    BottomUpCanonicalParserGenerator, \
    SLRParserGenerator, \
    LRParserGenerator, \
    LALRParserGenerator
from boson.system.logger import logger

parser_generator_library = {
    'slr': SLRParserGenerator,
    'lr': LRParserGenerator,
    'lalr': LALRParserGenerator,
}

code_generator_library = {
    'python': PythonCodeGenerator,
    'c++': CppCodeGenerator,
    'java': JavaCodeGenerator,
    'javascript': JavaScriptCodeGenerator
}

quiet = False


def display(text: str = '', indent: int = 0, newline: bool = True, file=sys.stdout) -> None:
    if not quiet:
        print(' ' * indent + text, end=('\n' if newline else ''), flush=True, file=file)


def welcome() -> None:
    display('{} - {}'.format(configure.boson_title, configure.boson_description))
    display('Author: {}'.format(configure.boson_author), indent=4)
    display('Email:  {}'.format(configure.boson_email), indent=4)
    display('URL:    {}'.format(configure.boson_url), indent=4)
    display()


def console_main() -> None:
    argument_parser = argparse.ArgumentParser(
        prog=configure.boson_name.lower(),
        description='{} - {}'.format(configure.boson_title, configure.boson_description),
        formatter_class=RawTextHelpFormatter)
    argument_parser.add_argument(
        'boson_script_file',
        help='Input Boson Script File.')
    argument_parser.add_argument(
        '-o', '--output', default='boson',
        help='Output Boson Code Path(Default Is `boson`).')
    argument_parser.add_argument(
        '-q', '--quiet', action='store_true',
        help='Display Nothing.')
    arguments = argument_parser.parse_args()
    global quiet
    quiet = arguments.quiet
    welcome()
    source_file = None
    logger.initialize()
    try:
        display('[Generate Analyzer Code]')
        step = 1
        display('[{}] Parse Boson Script... '.format(step), indent=4, newline=False)
        start_time = time.time()
        global_start_time = start_time
        source_file = open(arguments.boson_script_file, 'r', encoding=configure.boson_default_encoding)
        script_analyzer = BosonScriptAnalyzer()
        script_analyzer.tokenize_and_parse(source_file.read())
        command_executor = CommandExecutor()
        command_executor.execute(script_analyzer.command_list())
        end_time = time.time()
        display('Done [{:.4f}s]'.format(end_time - start_time))
        display('> Commands Count: {}'.format(len(script_analyzer.command_list())), indent=8)
        display('> Lexical Definition: {}'.format('Yes' if script_analyzer.lexical_definition() else 'No'), indent=8)
        display('> Grammar Definition: {}'.format('Yes' if script_analyzer.sentence_set() else 'No'), indent=8)
        if boson_option['code']['generate']['lexer'] == 'True' and script_analyzer.lexical_definition():
            step += 1
            display('[{}] Generate Lexical Analysis Table... '.format(step), indent=4, newline=False)
            start_time = time.time()
            lexical_analyzer = LexerGenerator(script_analyzer.lexical_definition())
            lexical_analyzer.generate_lexical_dfa()
            lexical_analyzer.generate_compact_move_table()
            end_time = time.time()
            display('Done [{:.4f}s]'.format(end_time - start_time))
            display('> Lexical Definition Count: {}'.format(len(script_analyzer.lexical_definition())), indent=8)
            display('> Character Set Size: {}'.format(len(lexical_analyzer.character_set())), indent=8)
            display('> DFA State Count: {}'.format(len(lexical_analyzer.compact_move_table())), indent=8)
        else:
            lexical_analyzer = None
        if script_analyzer.sentence_set():
            step += 1
            display('[{}] Generate Grammar Analysis Table... '.format(step), indent=4, newline=False)
            start_time = time.time()
            parser_generator = parser_generator_library[boson_option['parser']['analyzer']](script_analyzer.sentence_set(), script_analyzer.sentence_attribute_mapping())
            parser_generator.initialize()
            parser_generator.assemble_sentence_grammar_name(script_analyzer.sentence_grammar_name_mapping())
            parser_generator.assemble_grammar_tuple(script_analyzer.sentence_grammar_tuple_mapping())
            parser_generator.assemble_naive_sentence(script_analyzer.naive_sentence_set())
            parser_generator.generate_parser_dfa()
            parser_generator.generate_parse_table()
            parser_generator.parse_table_sparsification()
            end_time = time.time()
            display('Done [{:.4f}s]'.format(end_time - start_time))
            display('> Algorithm: {}'.format(boson_option['parser']['analyzer'].upper()), indent=8)
            display('> Grammar Sentence Count: {}'.format(len(parser_generator.sentence_set()) - 1), indent=8)
            display('> Non-Terminal Symbol Count: {}'.format(len(parser_generator.non_terminal_set())), indent=8)
            display('> Terminal Symbol Count: {}'.format(len(parser_generator.terminal_set())), indent=8)
            if isinstance(parser_generator, BottomUpParserGenerator):
                display('> PDA State Count: {}'.format(len(parser_generator.state_reduce_mapping())), indent=8)
                if isinstance(parser_generator, BottomUpCanonicalParserGenerator):
                    action_table_size = sum([len(line) for line in parser_generator.action_table()])
                    sparse_action_table_size = sum([len(line) for _, line in parser_generator.sparse_action_table().items()])
                    action_table_compression_rate = sparse_action_table_size / action_table_size * 100 if action_table_size > 0 else 0
                    goto_table_size = sum([len(line) for line in parser_generator.goto_table()])
                    sparse_goto_table_size = sum([len(line) for _, line in parser_generator.sparse_goto_table().items()])
                    goto_table_compression_rate = sparse_goto_table_size / goto_table_size * 100 if goto_table_size > 0 else 0
                    display('> Action Table Size/Sparse-Size (Rate): {}/{} ({:.2f}%)'.format(action_table_size, sparse_action_table_size, action_table_compression_rate), indent=8)
                    display('> Goto Table Size/Sparse-Size (Rate): {}/{} ({:.2f}%)'.format(goto_table_size, sparse_goto_table_size, goto_table_compression_rate), indent=8)
            if parser_generator.conflict_list():
                conflict_type_text = {
                    configure.boson_conflict_reduce_reduce: 'Reduce/Reduce',
                    configure.boson_conflict_shift_reduce: 'Shift/Reduce'
                }
                display('[Error] Conflict', indent=4)
                for state_number, conflict_type, terminal in parser_generator.conflict_list():
                    if terminal in script_analyzer.literal_reverse_mapping():
                        terminal = '\'{}\''.format(script_analyzer.literal_reverse_mapping()[terminal])
                    display('[Conflict State: {}] <{}> Terminal: {}'.format(state_number, conflict_type_text[conflict_type], terminal), indent=8)
                return
        else:
            parser_generator = None
        step += 1
        display('[{}] Generate Code... '.format(step), indent=4, newline=False)
        start_time = time.time()
        if not os.path.isdir(arguments.output):
            os.mkdir(arguments.output)
        code_generator = code_generator_library[boson_option['code']['language']](arguments.output, boson_option['mode'], boson_option['code']['checker'] == 'True')
        if lexical_analyzer is not None:
            code_generator.dispose_lexer(lexical_analyzer)
        if parser_generator is not None:
            code_generator.dispose_parser(parser_generator)
        code_generator.generate_code()
        end_time = time.time()
        display('Done [{:.4f}s]'.format(end_time - start_time))
        display('> Language: {}'.format(boson_option['code']['language'].upper()), indent=8)
        display('> Mode: {}'.format(boson_option['mode'].capitalize()), indent=8)
        display('> Checker: {}'.format('Yes' if boson_option['code']['checker'] == 'True' else 'No'), indent=8)
        display('> Generate Lexer: {}'.format('Yes' if lexical_analyzer else 'No'), indent=8)
        display('> Generate Parser: {}'.format('Yes' if parser_generator else 'No'), indent=8)
        display('> Generate Interpreter: {}'.format('Yes' if parser_generator and boson_option['code']['generate']['interpreter'] == 'True' else 'No'), indent=8)
        display('> Output Path: "{}"'.format(arguments.output), indent=8)
        global_end_time = time.time()
        display('[Complete!!! {:.4f}s]'.format(global_end_time - global_start_time))
        display()
    except ValueError as e:
        logger.error(str(e))
        display('\n\n[Error] {}'.format(e), file=sys.stderr)
    except Exception as e:
        logger.error_block(traceback.format_exc())
        display('\n\n[Error] {}'.format(repr(e)), file=sys.stderr)
    finally:
        logger.close()
        if source_file is not None:
            source_file.close()
