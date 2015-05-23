__author__ = 'ict'


from boson.bs_grammar_analysis import bs_token_list, bs_grammar_analyzer
from boson.bs_slr_generate import bs_slr_generate_table
from boson.bs_lr_generate import bs_lr_generate_table
from boson.bs_lalr_generate import bs_lalr_generate_table
from boson.bs_code_generate import bs_generate_python_code
from boson.bs_lexcial_analyzer import BosonLexicalAnalyzer


if __name__ == "__main__":
    lex = BosonLexicalAnalyzer("test/lex.txt")
    token_list, literal = bs_token_list("test/slr_grammar.txt")
    sentence_set, reduce_code, command_list = bs_grammar_analyzer(token_list)
    slr_tables = bs_slr_generate_table(sentence_set)
    bs_generate_python_code(slr_tables, reduce_code, literal, lex=lex)
    token_list, literal = bs_token_list("test/not_slr_grammar.txt")
    sentence_set, reduce_code, command_list = bs_grammar_analyzer(token_list)
    lr_tables = bs_lr_generate_table(sentence_set)
    bs_generate_python_code(lr_tables, reduce_code, literal, lex=lex)
    token_list, literal = bs_token_list("test/not_slr_grammar.txt")
    sentence_set, reduce_code, command_list = bs_grammar_analyzer(token_list)
    lalr_tables = bs_lalr_generate_table(sentence_set)
    bs_generate_python_code(lalr_tables, reduce_code, literal, lex=lex)
    token_list, literal = bs_token_list("test/literal_grammar.txt")
    sentence_set, reduce_code, command_list = bs_grammar_analyzer(token_list)
    lalr_tables = bs_lalr_generate_table(sentence_set)
    bs_generate_python_code(lalr_tables, reduce_code, literal, lex=lex)
