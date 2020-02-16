import jinja2
import math
import boson.bs_configure as configure
from boson.bs_data_package import AnalyzerTable, LexicalPackage, GrammarPackage


def bs_generate_code(language: str, analyzer_table: AnalyzerTable, lexical_package: (LexicalPackage, None), grammar_package: GrammarPackage) -> str:
    none_grammar_tuple_reduce = [analyzer_table.sentence_list.index(sentence) for sentence in grammar_package.none_grammar_tuple_set]
    none_grammar_tuple_reduce.sort()
    none_grammar_tuple_reduce = list(map(str, none_grammar_tuple_reduce))
    sparse_table = configure.boson_option['sparse_table'] == 'yes'
    generate_semantics_analyzer = configure.boson_option['generate_semantics_analyzer'] == 'yes'
    generate_lexical_analyzer = configure.boson_option['generate_lexical_analyzer'] == 'yes' and isinstance(lexical_package, LexicalPackage)
    if sparse_table:
        sparse_action_table = {}
        action_table = analyzer_table.action_table
        for i, sub_table in enumerate(action_table):
            sparse_sub_table = {}
            for j, action in enumerate(sub_table):
                if action != configure.boson_table_sign_error:
                    sparse_sub_table[j] = action
            if sparse_sub_table:
                sparse_action_table[i] = sparse_sub_table
        analyzer_table.action_table = sparse_action_table
        sparse_goto_table = {}
        goto_table = analyzer_table.goto_table
        for i, sub_table in enumerate(goto_table):
            sparse_sub_table = {}
            for j, state in enumerate(sub_table):
                if state != configure.boson_invalid_goto:
                    sparse_sub_table[j] = state
            if sparse_sub_table:
                sparse_goto_table[i] = sparse_sub_table
        analyzer_table.goto_table = sparse_goto_table
    reduce_number_to_grammar_name = {}
    reduce_number_to_grammar_number = {}
    naive_reduce_number = set()
    if generate_semantics_analyzer:
        for sentence, grammar_sign in grammar_package.sentence_grammar_map.items():
            reduce_number = analyzer_table.sentence_list.index(sentence)
            if isinstance(grammar_sign, int):
                reduce_number_to_grammar_number[reduce_number] = grammar_sign
            elif isinstance(grammar_sign, str):
                reduce_number_to_grammar_name[reduce_number] = grammar_sign
            else:
                raise ValueError('Invalid grammar sign type: {}'.format(type(grammar_sign)))
        for sentence in grammar_package.naive_sentence:
            naive_reduce_number.add(analyzer_table.sentence_list.index(sentence))
    template_data = {
        'configure': configure,
        'analyzer_table': analyzer_table,
        'grammar_package': grammar_package,
        'reduce_number_width': int(math.log10(len(analyzer_table.sentence_list))) + 1,
        'none_grammar_tuple_reduce': none_grammar_tuple_reduce,
        'have_default_reduce_tuple': len(grammar_package.none_grammar_tuple_set) != 0,
        'have_special_generate': len(grammar_package.grammar_tuple_map) != 0,
        'reduce_number_to_grammar_name': reduce_number_to_grammar_name,
        'reduce_number_to_grammar_number': reduce_number_to_grammar_number,
        'naive_reduce_number': naive_reduce_number,
        'sparse_table': sparse_table,
        'code_comment': configure.boson_option['code_comment'] == 'yes',
        'generate_semantics_analyzer': generate_semantics_analyzer,
        'generate_lexical_analyzer': generate_lexical_analyzer,
        'lexical_package': lexical_package
    }
    environment = jinja2.Environment(loader=jinja2.PackageLoader(configure.boson_package_name, configure.boson_template_directory))
    template = environment.get_template(language + configure.boson_template_postfix)
    code_text = template.render(template_data)
    return code_text


def bs_generate_python3_code(analyzer_table: AnalyzerTable, lexical_package: LexicalPackage, grammar_package: GrammarPackage) -> str:
    return bs_generate_code('python3', analyzer_table, lexical_package, grammar_package)


def bs_generate_cpp_code(analyzer_table: AnalyzerTable, lexical_package: LexicalPackage, grammar_package: GrammarPackage) -> str:
    return bs_generate_code('c++', analyzer_table, lexical_package, grammar_package)
