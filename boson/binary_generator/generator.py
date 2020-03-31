from struct import pack


class BinaryGenerator:
    def __init__(self):
        pass

    @staticmethod
    def length(number: int) -> (int, str):
        if number <= 0xff:
            return 1, 'B'
        elif number <= 0xffff:
            return 2, 'H'
        elif number <= 0xffffffff:
            return 4, 'I'
        else:
            return 8, 'Q'

    @staticmethod
    def pack_list(element_type: str, list_like_container, nest: bool = False) -> bytes:
        list_body_bytes = bytes()
        for element in list_like_container:
            list_body_bytes += pack(element_type, *element) if nest else pack(element_type, element)
        list_body_length = len(list_body_bytes)
        length, pack_type = BinaryGenerator.length(list_body_length)
        return pack('B{}{}s'.format(pack_type, list_body_length), length, list_body_length, list_body_bytes)

    @staticmethod
    def pack_mapping(key_pack_function: callable, value_pack_function: callable, mapping_container: dict) -> bytes:
        mapping_body_bytes = bytes()
        for key, value in mapping_container.items():
            key_pack = key_pack_function(key)
            value_pack = value_pack_function(value)
            mapping_body_bytes += pack('{}s{}s'.format(len(key_pack), len(value_pack)), value_pack)
        mapping_body_length = len(mapping_body_bytes)
        length, pack_type = BinaryGenerator.length(mapping_body_length)
        return pack('B{}{}s'.format(pack_type, mapping_body_length), length, mapping_body_length, mapping_body_bytes)
