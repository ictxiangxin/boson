__author__ = 'ict'


from boson.bs_grammmar_analysis import bs_token_list, bs_grammar_analyzer
from boson.bs_slr_generate import bs_slr_generate_table
from boson.bs_lr_generate import bs_lr_generate_table
from boson.bs_lalr_generate import bs_lalr_generate_table
from boson.bs_code_generate import bs_generate_python_code


if __name__ == "__main__":
    token_list = bs_token_list("test/slr_grammar.txt")
    sentence_set, reduce_code = bs_grammar_analyzer(token_list)
    slr_tables = bs_slr_generate_table(sentence_set)
    bs_generate_python_code(slr_tables, reduce_code)
    token_list = bs_token_list("test/not_slr_grammar.txt")
    sentence_set, reduce_code = bs_grammar_analyzer(token_list)
    lr_tables = bs_lr_generate_table(sentence_set)
    bs_generate_python_code(lr_tables, reduce_code)
    token_list = bs_token_list("test/not_slr_grammar.txt")
    sentence_set, reduce_code = bs_grammar_analyzer(token_list)
    lalr_tables = bs_lalr_generate_table(sentence_set)
    bs_generate_python_code(lalr_tables, reduce_code)
