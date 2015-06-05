__author__ = 'ict'


from boson.bs_grammar_analysis import bs_token_list, bs_grammar_analyzer
from boson.bs_slr_generate import bs_slr_generate_table
from boson.bs_lr_generate import bs_lr_generate_table
from boson.bs_lalr_generate import bs_lalr_generate_table
from boson.bs_code_generate import bs_generate_python_code
from boson.bs_lexcial_analyzer import BosonLexicalAnalyzer
from boson.bs_ebnf_to_bnf import bs_ebnf_to_bnf


if __name__ == "__main__":
    lex = BosonLexicalAnalyzer("test/lex.txt")
    token_list = bs_token_list("test/slr_grammar.txt")
    data_package = bs_grammar_analyzer(token_list)
    sentence_set = data_package["sentence set"]
    reduce_code = data_package["reduce code"]
    command_list = data_package["command list"]
    literal = (data_package["literal map"], data_package["literal reverse map"])
    slr_tables = bs_slr_generate_table(sentence_set)
    bs_generate_python_code(slr_tables, data_package, lex=lex)
    token_list = bs_token_list("test/not_slr_grammar.txt")
    data_package = bs_grammar_analyzer(token_list)
    sentence_set = data_package["sentence set"]
    reduce_code = data_package["reduce code"]
    command_list = data_package["command list"]
    literal = (data_package["literal map"], data_package["literal reverse map"])
    lr_tables = bs_lr_generate_table(sentence_set)
    bs_generate_python_code(lr_tables, data_package, lex=lex)
    token_list = bs_token_list("test/not_slr_grammar.txt")
    data_package = bs_grammar_analyzer(token_list)
    sentence_set = data_package["sentence set"]
    reduce_code = data_package["reduce code"]
    command_list = data_package["command list"]
    literal = (data_package["literal map"], data_package["literal reverse map"])
    lalr_tables = bs_lalr_generate_table(sentence_set)
    bs_generate_python_code(lalr_tables, data_package, lex=lex)
    token_list = bs_token_list("test/literal_grammar.txt")
    data_package = bs_grammar_analyzer(token_list)
    sentence_set = data_package["sentence set"]
    reduce_code = data_package["reduce code"]
    command_list = data_package["command list"]
    literal = (data_package["literal map"], data_package["literal reverse map"])
    lalr_tables = bs_lalr_generate_table(sentence_set)
    bs_generate_python_code(lalr_tables, data_package, lex=lex)
    bs_ebnf_to_bnf("test/ebnf.txt")
