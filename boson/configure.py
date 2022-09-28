boson_name = 'Boson'
boson_package_name = 'boson'
boson_version_major = 1
boson_version_minor = 7
boson_title = f'{boson_name} v{boson_version_major}.{boson_version_minor}'
boson_author = 'ict'
boson_email = 'ictxiangxin@hotmail.com'
boson_url = 'https://github.com/ictxiangxin/boson'
boson_description = 'Grammar Analyzer Generator'
boson_license = 'GPL v3'

boson_default_encoding = 'utf-8'

boson_template_directory = 'code_generator/templates'
boson_template_postfix = '.template'

boson_table_sign_error = 'e'
boson_table_sign_shift = 's'
boson_table_sign_reduce = 'r'
boson_table_sign_accept = 'a'
boson_invalid_goto = -1

boson_conflict_reduce_reduce = 0
boson_conflict_shift_reduce = 1
boson_check_pass_index = -1

boson_grammar_tuple_prefix = '$'
boson_grammar_tuple_unpack = '*'
boson_grammar_no_error_index = -1
boson_grammar_default_reduce_number = -1
boson_grammar_default_state = 0

boson_lexical_reserved_character = chr(0x10ffff)
boson_lexical_hidden_prefix = '_'
boson_lexical_start_line = 1
boson_lexical_default_skip = False
boson_lexical_no_error_index = -1
boson_lexical_default_state = 0
boson_lexical_default_start_state = 0
boson_lexical_default_end_state = 1
boson_lexical_epsilon_transition = None
boson_lexical_wildcard = True
boson_lexical_non_greedy_sign = '!'

boson_reserved_symbol = '!'
boson_end_symbol = '$'
boson_null_symbol = '~'

boson_symbol_template = f'{boson_reserved_symbol}symbol_{{}}'
boson_augmented_start = f'{boson_reserved_symbol}start'
boson_hidden_name_prefix = f'{boson_reserved_symbol}name_'
boson_operator_name_prefix = f'{boson_reserved_symbol}operator_'
boson_grammar_name_prefix = f'{boson_reserved_symbol}grammar_'
boson_default_symbol = f'{boson_reserved_symbol}symbol'

boson_log_file_default_path = '.'
