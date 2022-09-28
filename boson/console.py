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
    display(f'{configure.boson_title} - {configure.boson_description}')
    display(f'Author: {configure.boson_author}', indent=4)
    display(f'Email:  {configure.boson_email}', indent=4)
    display(f'URL:    {configure.boson_url}', indent=4)
    display()


def console_main() -> None:
    argument_parser = argparse.ArgumentParser(
        prog=configure.boson_name.lower(),
        description=f'{configure.boson_title} - {configure.boson_description}',
        formatter_class=RawTextHelpFormatter)
    argument_parser.add_argument(
        'boson_script_file',
        help='Input Boson Script File.')
    argument_parser.add_argument(
        '-o', '--output', default='boson',
        help='Output Boson Code Path(Default Is `boson`).')
    argument_parser.add_argument(
        '-l', '--log', action='store_true',
        help='Enable Boson Log.')
    argument_parser.add_argument(
        '-q', '--quiet', action='store_true',
        help='Display Nothing.')
    arguments = argument_parser.parse_args()
    global quiet
    quiet = arguments.quiet
    welcome()
    source_file = None
    if arguments.log:
        logger.initialize()
    try:
        display('[Generate Analyzer Code]')
        step = 1
        display(f'[{step}] Parse Boson Script... ', indent=4, newline=False)
        start_time = time.time()
        global_start_time = start_time
        logger.info(f'[Boson] Open Boson Script File: File="{arguments.boson_script_file}"')
        source_file = open(arguments.boson_script_file, 'r', encoding=configure.boson_default_encoding)
        script_analyzer = BosonScriptAnalyzer()
        logger.info('[Boson] Parse Boson Script.')
        script_analyzer.tokenize_and_parse(source_file.read())
        command_executor = CommandExecutor()
        command_executor.execute(script_analyzer.command_list())
        end_time = time.time()
        display(f'Done [{end_time - start_time:.4f}s]')
        display(f'> Commands Count: {len(script_analyzer.command_list())}', indent=8)
        display(f'> Lexical Definition: {"Yes" if script_analyzer.lexical_definition() else "No"}', indent=8)
        display(f'> Grammar Definition: {"Yes" if script_analyzer.sentence_set() else "No"}', indent=8)
        if boson_option['code']['generator']['lexer'] == 'True' and script_analyzer.lexical_definition():
            step += 1
            display(f'[{step}] Generate Lexical Analysis Table... ', indent=4, newline=False)
            start_time = time.time()
            lexical_analyzer = LexerGenerator(script_analyzer.lexical_definition())
            lexical_analyzer.generate_lexical_dfa()
            lexical_analyzer.generate_compact_move_table()
            end_time = time.time()
            display(f'Done [{end_time - start_time:.4f}s]')
            display(f'> Lexical Definition Count: {len(script_analyzer.lexical_definition())}', indent=8)
            display(f'> Character Set Size: {len(lexical_analyzer.character_set())}', indent=8)
            display(f'> DFA State Count: {len(lexical_analyzer.compact_move_table())}', indent=8)
        else:
            lexical_analyzer = None
        if script_analyzer.sentence_set():
            step += 1
            display(f'[{step}] Generate Grammar Analysis Table... ', indent=4, newline=False)
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
            display(f'Done [{end_time - start_time:.4f}s]')
            display(f'> Algorithm: {boson_option["parser"]["analyzer"].upper()}', indent=8)
            display(f'> Grammar Sentence Count: {len(parser_generator.sentence_set()) - 1}', indent=8)
            display(f'> Non-Terminal Symbol Count: {len(parser_generator.non_terminal_set())}', indent=8)
            display(f'> Terminal Symbol Count: {len(parser_generator.terminal_set())}', indent=8)
            if isinstance(parser_generator, BottomUpParserGenerator):
                display(f'> PDA State Count: {len(parser_generator.state_reduce_mapping())}', indent=8)
                if isinstance(parser_generator, BottomUpCanonicalParserGenerator):
                    action_table_size = sum([len(line) for line in parser_generator.action_table()])
                    sparse_action_table_size = sum([len(line) for _, line in parser_generator.sparse_action_table().items()])
                    action_table_compression_rate = sparse_action_table_size / action_table_size * 100 if action_table_size > 0 else 0
                    goto_table_size = sum([len(line) for line in parser_generator.goto_table()])
                    sparse_goto_table_size = sum([len(line) for _, line in parser_generator.sparse_goto_table().items()])
                    goto_table_compression_rate = sparse_goto_table_size / goto_table_size * 100 if goto_table_size > 0 else 0
                    display(f'> Action Table Size/Sparse-Size (Rate): {action_table_size}/{sparse_action_table_size} ({action_table_compression_rate:.2f}%)', indent=8)
                    display(f'> Goto Table Size/Sparse-Size (Rate): {goto_table_size}/{sparse_goto_table_size} ({goto_table_compression_rate:.2f}%)', indent=8)
            if parser_generator.conflict_list():
                conflict_type_text = {
                    configure.boson_conflict_reduce_reduce: 'Reduce/Reduce',
                    configure.boson_conflict_shift_reduce: 'Shift/Reduce'
                }
                display('[Error] Conflict', indent=4)
                for state_number, conflict_type, terminal in parser_generator.conflict_list():
                    if terminal in script_analyzer.literal_reverse_mapping():
                        terminal = f'\'{script_analyzer.literal_reverse_mapping()[terminal]}\''
                    display(f'[Conflict State: {state_number}] <{conflict_type_text[conflict_type]}> Terminal: {terminal}', indent=8)
                return
        else:
            parser_generator = None
        step += 1
        display(f'[{step}] Generate Code... ', indent=4, newline=False)
        start_time = time.time()
        if not os.path.isdir(arguments.output):
            os.mkdir(arguments.output)
        code_generator = code_generator_library[boson_option['code']['language']](arguments.output, boson_option['mode'], boson_option['code']['checker'] == 'True')
        if lexical_analyzer is not None:
            code_generator.dispose_lexer(lexical_analyzer)
        if parser_generator is not None:
            code_generator.dispose_parser(parser_generator)
        code_generator.generate_code()
        logger.info(f'[Boson] Generate Target Code: Path="{arguments.output}"')
        end_time = time.time()
        display(f'Done [{end_time - start_time:.4f}s]')
        display(f'> Language: {boson_option["code"]["language"].upper()}', indent=8)
        display(f'> Mode: {boson_option["mode"].capitalize()}', indent=8)
        display(f'> Checker: {"Yes" if boson_option["code"]["checker"] == "True" else "No"}', indent=8)
        display(f'> Generate Lexer: {"Yes" if lexical_analyzer else "No"}', indent=8)
        display(f'> Generate Parser: {"Yes" if parser_generator else "No"}', indent=8)
        display(f'> Generate Interpreter: {"Yes" if parser_generator and boson_option["code"]["generator"]["interpreter"] == "True" else "No"}', indent=8)
        display(f'> Output Path: "{arguments.output}"', indent=8)
        global_end_time = time.time()
        display(f'[Complete!!! {global_end_time - global_start_time:.4f}s]')
        display()
    except ValueError as e:
        message = str(e)
        if '\n' in message:
            logger.error_block(message)
        else:
            logger.error(message)
        display(f'\n\n[Error] {e}', file=sys.stderr)
    except Exception as e:
        logger.error_block(traceback.format_exc())
        display(f'\n\n[Error] {repr(e)}', file=sys.stderr)
    finally:
        logger.close()
        if source_file is not None:
            source_file.close()
