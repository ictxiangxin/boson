import jinja2
import math
import boson.bs_configure as configure
from boson.bs_data_package import AnalyzerTable, GrammarPackage


def bs_generate_code(language: str, analyzer_table: AnalyzerTable, grammar_package: GrammarPackage):
    none_grammar_tuple_reduce = [analyzer_table.sentence_list.index(sentence) for sentence in grammar_package.none_grammar_tuple_set]
    none_grammar_tuple_reduce.sort()
    none_grammar_tuple_reduce = list(map(str, none_grammar_tuple_reduce))
    template_data = {
        "title": configure.boson_title,
        "description": configure.boson_description,
        "author": configure.boson_author,
        "email": configure.boson_author_email,
        "table_sign_error": configure.boson_table_sign_error,
        "table_sign_shift": configure.boson_table_sign_shift,
        "table_sign_reduce": configure.boson_table_sign_reduce,
        "table_sign_accept": configure.boson_table_sign_accept,
        "analyzer_class_name": configure.option["analyzer_class_name"],
        "grammar_class_name": configure.option["grammar_class_name"],
        "reduce_number_width": int(math.log10(len(analyzer_table.sentence_list))) + 1,
        "terminal_index": analyzer_table.terminal_index,
        "action_table": analyzer_table.action_table,
        "goto_table": analyzer_table.goto_table,
        "reduce_symbol_sum": analyzer_table.reduce_symbol_sum,
        "reduce_to_non_terminal_index": analyzer_table.reduce_to_non_terminal_index,
        "sentence_list": analyzer_table.sentence_list,
        "grammar_tuple_map": grammar_package.grammar_tuple_map,
        "literal_reverse_map": grammar_package.literal_reverse_map,
        "none_grammar_tuple_reduce": none_grammar_tuple_reduce,
        "have_default_reduce_tuple": len(grammar_package.none_grammar_tuple_set) != 0,
        "no_special_generate": len(grammar_package.grammar_tuple_map) == 0,
    }
    environment = jinja2.Environment(loader=jinja2.PackageLoader(configure.boson_package_name, configure.boson_template_directory))
    template = environment.get_template(language + configure.boson_template_postfix)
    code_text = template.render(template_data)
    return code_text


def bs_generate_python3_code(analyzer_table: AnalyzerTable, grammar_package: GrammarPackage):
    return bs_generate_code("python3", analyzer_table, grammar_package)
