from .semantic_node import BosonSemanticsNode
from .grammar_node import BosonGrammarNode


class BosonInterpreter:
    def __init__(self):
        self.__reduce_number_grammar_name_mapping: dict = {
            30: 'command',
            27: 'lexical_define',
            74: 'reduce',
            82: 'getter_tuple',
            69: 'grammar_node',
            28: 'name_closure',
            21: 'literal',
            4: 'complex_closure',
            32: 'complex_optional',
            35: 'select',
            52: 'attribute',
            13: 'string',
            45: 'number',
            37: 'attribute_value_list'
        }
        self.__naive_reduce_number_set: set = {2, 6, 13, 14, 19, 21, 44, 45, 47, 48, 50, 57, 59, 70, 72, 75, 86, 87, 89}
        self.__semantic_action_mapping: dict = {}

    def __semantics_analysis(self, grammar_tree: BosonGrammarNode) -> BosonSemanticsNode:
        if grammar_tree.get_reduce_number() in self.__reduce_number_grammar_name_mapping:
            grammar_name = self.__reduce_number_grammar_name_mapping[grammar_tree.get_reduce_number()]
        else:
            grammar_name = '!grammar_hidden'
        semantic_node = BosonSemanticsNode()
        if len(grammar_tree.children()) == 0:
            semantic_node.set_reduce_number(grammar_tree.get_reduce_number())
            semantic_node.set_text(grammar_tree.get_text())
        else:
            for grammar_node in grammar_tree.children():
                semantic_node.append(self.__semantics_analysis(grammar_node))
        if grammar_name in self.__semantic_action_mapping:
            return self.__semantic_action_mapping[grammar_name](semantic_node)
        elif grammar_tree.get_reduce_number() in self.__naive_reduce_number_set:
            if len(semantic_node.children()) == 0:
                return BosonSemanticsNode.null_node()
            elif len(semantic_node.children()) == 1:
                return semantic_node[0]
            else:
                return semantic_node
        else:
            return semantic_node

    def execute(self, grammar_tree: BosonGrammarNode) -> BosonSemanticsNode:
        return self.__semantics_analysis(grammar_tree)

    def register_action(self, name: str) -> callable:
        def decorator(f: callable):
            self.__semantic_action_mapping[name] = f
            return f
        return decorator
