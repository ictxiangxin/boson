from typing import Dict, Set

from .semantic_node import BosonSemanticsNode
from .grammar_node import BosonGrammarNode


class BosonInterpreter:
    def __init__(self):
        self.__reduce_number_grammar_name_mapping: Dict[int, str] = {
            31: 'command',
            63: 'lexical_define',
            59: 'reduce',
            29: 'getter_tuple',
            75: 'grammar_node',
            35: 'element_definition',
            87: 'name_closure',
            7: 'literal',
            56: 'regular',
            106: 'complex_closure',
            92: 'complex_optional',
            37: 'select',
            42: 'attribute',
            79: 'string',
            102: 'number',
            36: 'attribute_value_list'
        }
        self.__naive_reduce_number_set: Set[int] = {101, 102, 7, 73, 12, 79, 16, 81, 47, 48, 84, 53, 49, 18, 25, 90}
        self.__semantic_action_mapping: Dict[str, callable] = {}

    def __semantics_analysis(self, grammar_tree: BosonGrammarNode) -> BosonSemanticsNode:
        if grammar_tree.get_reduce_number() in self.__reduce_number_grammar_name_mapping:
            grammar_name: str = self.__reduce_number_grammar_name_mapping[grammar_tree.get_reduce_number()]
        else:
            grammar_name: str = '!grammar_hidden'
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
