class BosonSemanticsNode:
    def __init__(self, data=None):
        self.__reduce_number: int = -1
        self.__text: str = ''
        self.__children: list = []
        self.__data = data
        self.__is_null: bool = False

    def __getitem__(self, index):
        return self.__children[index]

    def make_null(self) -> None:
        self.__is_null = True

    def is_null(self) -> bool:
        return self.__is_null

    def get_data(self):
        return self.__data

    def set_data(self, data):
        self.__data = data

    def get_reduce_number(self) -> int:
        return self.__reduce_number

    def set_reduce_number(self, reduce_number) -> None:
        self.__reduce_number = reduce_number

    def get_text(self) -> str:
        return self.__text

    def set_text(self, text) -> None:
        self.__text = text

    def append(self, item) -> None:
        self.__children.append(item)

    def insert(self, index, item) -> None:
        self.__children.insert(index, item)

    def children(self) -> list:
        return self.__children

    @staticmethod
    def null_node():
        node = BosonSemanticsNode()
        node.make_null()
        return node
