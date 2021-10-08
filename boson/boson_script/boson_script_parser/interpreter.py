from .semantic_node import BosonSemanticsNode
from .grammar_node import BosonGrammarNode


class BosonInterpreter:
    def __init__(self):
        self.__reduce_number_grammar_name_mapping: dict = {
            4: 'command',
            39: 'lexical_define',
            46: 'reduce',
            25: 'getter_tuple',
            5: 'grammar_node',
            30: 'name_closure',
            26: 'literal',
            86: 'complex_closure',
            35: 'complex_optional',
            76: 'select',
            43: 'attribute',
            91: 'string',
            62: 'number',
            88: 'attribute_value_list'
        }
        self.__naive_reduce_number_set: set = {7, 13, 16, 19, 22, 26, 27, 29, 32, 33, 34, 36, 56, 60, 62, 63, 65, 75, 91}
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
