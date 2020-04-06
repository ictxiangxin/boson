class BosonGrammarNode:
    def __init__(self, text: str = ''):
        self.__reduce_number = -1
        self.__children: list = []
        self.__text: str = text

    def __getitem__(self, item):
        return self.__children[item]

    def get_reduce_number(self) -> int:
        return self.__reduce_number

    def set_reduce_number(self, reduce_number: int) -> None:
        self.__reduce_number = reduce_number

    def get_text(self) -> str:
        return self.__text

    def set_text(self, text: str) -> None:
        self.__text = text

    def append(self, item) -> None:
        self.__children.append(item)

    def insert(self, index, item) -> None:
        self.__children.insert(index, item)

    def children(self) -> list:
        return self.__children
