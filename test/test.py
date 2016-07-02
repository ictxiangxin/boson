from boson.bs_grammar_analysis import bs_grammar_analysis
from boson.bs_slr_generate import bs_slr_generate_table
from boson.bs_lr_generate import bs_lr_generate_table
from boson.bs_lalr_generate import bs_lalr_generate_table
from boson.bs_code_generator import bs_generate_python3_code


if __name__ == "__main__":
    grammar_package = bs_grammar_analysis("test/slr_grammar.txt")
    slr_grammar_tables = bs_slr_generate_table(grammar_package.sentence_set)
    code = bs_generate_python3_code(slr_grammar_tables, grammar_package)
    print(code)
    grammar_package = bs_grammar_analysis("test/not_slr_grammar.txt")
    lr_grammar_tables = bs_lr_generate_table(grammar_package.sentence_set)
    code = bs_generate_python3_code(lr_grammar_tables, grammar_package)
    print(code)
    grammar_package = bs_grammar_analysis("test/not_slr_grammar.txt")
    lalr_grammar_tables = bs_lalr_generate_table(grammar_package.sentence_set)
    code = bs_generate_python3_code(lalr_grammar_tables, grammar_package)
    print(code)
    grammar_package = bs_grammar_analysis("test/literal_grammar.txt")
    lalr_tables = bs_lalr_generate_table(grammar_package.sentence_set)
    code = bs_generate_python3_code(lalr_tables, grammar_package)
    print(code)
