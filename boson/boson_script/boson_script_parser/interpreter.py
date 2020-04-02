from .grammar_node import BosonGrammarNode


class BosonInterpreter:
    def __init__(self):
        self.__reduce_number_grammar_name_mapping: dict = {
            4: 'command',
            44: 'lexical_define',
            58: 'reduce',
            66: 'grammar_node',
            54: 'name_closure',
            61: 'literal',
            9: 'complex_closure',
            10: 'complex_optional',
            51: 'select'
        }
        self.__naive_reduce_number_set: set = {67, 38, 39, 8, 45, 46, 15, 20, 22, 23, 25, 59, 61, 31}
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
