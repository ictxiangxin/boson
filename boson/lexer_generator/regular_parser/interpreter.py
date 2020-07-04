from .semantic_node import BosonSemanticsNode
from .grammar_node import BosonGrammarNode


class RegularInterpreter:
    def __init__(self):
        self.__reduce_number_grammar_name_mapping: dict = {
            32: 'regular_expression',
            27: 'expression',
            9: 'branch',
            37: 'group',
            14: 'simple_construct',
            22: 'wildcard_character',
            12: 'select',
            18: 'reference',
            26: 'construct_number'
        }
        self.__naive_reduce_number_set: set = {32, 33, 38, 6, 10, 11, 14, 15, 17, 18, 20, 22, 23, 25}
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
