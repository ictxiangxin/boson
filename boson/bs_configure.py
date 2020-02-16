boson_name = 'Boson'
boson_package_name = 'boson'
boson_version_main = 1
boson_version_sub = 2
boson_title = '{} v{}.{}'.format(boson_name, boson_version_main, boson_version_sub)
boson_author = 'ict'
boson_email = 'ictxiangxin@hotmail.com'
boson_url = 'https://github.com/ictxiangxin/boson'
boson_description = 'Grammar analyzer generator'
boson_license = 'GPL v3'

boson_template_directory = 'templates'
boson_template_postfix = '.template'

boson_table_sign_error = 'e'
boson_table_sign_shift = 's'
boson_table_sign_reduce = 'r'
boson_table_sign_accept = 'a'
boson_invalid_goto = -1

boson_conflict_reduce_reduce = 0
boson_conflict_shift_reduce = 1

boson_grammar_tuple_prefix = '$'
boson_grammar_tuple_number = '$'
boson_grammar_tuple_all = '?'
boson_grammar_tuple_unpack = '*'
boson_grammar_no_error_index = -1

boson_lexical_hidden_prefix = '_'
boson_lexical_start_line = 1
boson_lexical_default_skip = False
boson_lexical_no_error_line = -1
boson_lexical_default_state = 0
boson_lexical_default_start_state = 0
boson_lexical_default_end_state = 1
boson_lexical_epsilon_transition = None
boson_lexical_wildcard = True

boson_reserved_symbol = '!'
boson_end_symbol = '$'
boson_null_symbol = '~'

boson_symbol_template = '{}symbol_{}'.format(boson_reserved_symbol, '{}')
boson_augmented_start = '{}start'.format(boson_reserved_symbol)
boson_hidden_name_prefix = '{}name_'.format(boson_reserved_symbol)
boson_grammar_name_prefix = '{}grammar_'.format(boson_reserved_symbol)
boson_default_symbol = '{}symbol'.format(boson_reserved_symbol)

boson_option = {
    'start_symbol': 'start',
    'lexical_analyzer_class_name': 'BosonLexicalAnalyzer',
    'lexical_token_class_name': 'BosonToken',
    'grammar_analyzer_class_name': 'BosonGrammarAnalyzer',
    'grammar_class_name': 'BosonGrammar',
    'grammar_node_class_name': 'BosonGrammarNode',
    'semantics_analyzer_class_name': 'BosonSemanticsAnalyzer',
    'semantics_node_class_name': 'BosonSemanticsNode',
    'generate_semantics_analyzer': 'yes',
    'generate_lexical_analyzer': 'yes',
    'code_comment': 'yes',
    'sparse_table': 'yes',
    'conflict_resolver': 'no',
    'shift_reduce_conflict_resolver': 'shift',
    'reduce_reduce_conflict_resolver': 'long',
}

boson_option_enumeration = {
    'start_symbol': None,
    'lexical_analyzer_class_name': None,
    'lexical_token_class_name': None,
    'grammar_analyzer_class_name': None,
    'grammar_class_name': None,
    'grammar_node_class_name': None,
    'semantics_analyzer_class_name': None,
    'semantics_node_class_name': None,
    'generate_semantics_analyzer': {'yes', 'no'},
    'generate_lexical_analyzer': {'yes', 'no'},
    'code_comment': {'yes', 'no'},
    'sparse_table': {'yes', 'no'},
    'conflict_resolver': {'yes', 'no'},
    'shift_reduce_conflict_resolver': {'shift', 'reduce'},
    'reduce_reduce_conflict_resolver': {'long', 'short'},
}
