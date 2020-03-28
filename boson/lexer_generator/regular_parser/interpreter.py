from .grammar_node import BosonGrammarNode


class RegularInterpreter:
    def __init__(self):
        self.__reduce_number_grammar_name_mapping: dict = {
            32: 'regular_expression',
            13: 'expression',
            36: 'branch',
            28: 'group',
            21: 'simple_construct',
            37: 'complex_construct',
            5: 'wildcard_character',
            24: 'select',
            29: 'sub_expression',
            2: 'reference',
            17: 'count_range',
            19: 'construct_number'
        }
        self.__naive_reduce_number_set: set = {32, 2, 34, 3, 37, 5, 8, 16, 18, 20, 21, 25, 31}
        self.__semantic_action_mapping: dict = {}

    def __semantic_analysis(self, grammar_tree: BosonGrammarNode):
        if grammar_tree.reduce_number in self.__reduce_number_grammar_name_mapping:
            grammar_name = self.__reduce_number_grammar_name_mapping[grammar_tree.reduce_number]
        else:
            grammar_name = '!grammar_hidden'
        semantic_node_list = []
        for grammar_node in grammar_tree.data():
            if isinstance(grammar_node, BosonGrammarNode):
                semantic_node = self.__semantic_analysis(grammar_node)
            else:
                semantic_node = grammar_node
            semantic_node_list.append(semantic_node)
        if grammar_name in self.__semantic_action_mapping:
            return self.__semantic_action_mapping[grammar_name](semantic_node_list)
        elif grammar_tree.reduce_number in self.__naive_reduce_number_set:
            if len(semantic_node_list) == 0:
                return None
            elif len(semantic_node_list) == 1:
                return semantic_node_list[0]
            else:
                return semantic_node_list
        else:
            return semantic_node_list

    def execute(self, grammar_tree: BosonGrammarNode):
        return self.__semantic_analysis(grammar_tree)

    def register_action(self, name: str) -> callable:
        def decorator(f: callable):
            self.__semantic_action_mapping[name] = f
            return f
        return decorator
