__author__ = 'ict'

end_symbol = "$"
null_symbol = "~"

literal_templet = "literal%d"

boson_name = "Boson"
boson_version_main = 0
boson_version_sub = 5
boson_title = "%s v%d.%d" % (boson_name, boson_version_main, boson_version_sub)
boson_author = "ict"
boson_author_email = "ictxiangxin@gmail.com"

invalid_token_class = "boson_invalid"

boson_table_sign_error = "e"
boson_table_sign_shift = "s"
boson_table_sign_reduce = "r"
boson_table_sign_accept = "a"

configure = {
    "start_symbol":          "start",
    "grammar_analyzer_name": "boson_grammar_analysis",
    "lexical_analyzer_name": "boson_lexical_analysis",
    "symbol_stack_name":     "boson_stack",
    "generate_comment":      True,
    "have_line_number":      True,
    "indent_string":         " ",
    "indent_number":         4,
    "symbol_type":           None,
    "reduce_mode":           "common",
}
