from core.exceptions import InvalidAsciiCharacterException


class AsciiToBinaryMixin:

    @staticmethod
    def convert_ascii_to_binary_matrix(ascii_string: str) -> list[list[int]]:
        """
        Converts an ASCII string into a binary matrix based on the following characteristics:
        - a dash "-" is converted to zero "0"
        - a circle "o" is converted to one "1"

        For instance, this ASCII input would get converted to its corresponding binary matrix:
        --o--      00100
        -ooo-  ->  01110
        --o--      00100

        :param ascii_string: The ASCII string to convert.
        :return: The converted binary matrix.
        """
        if not ascii_string:
            return []

        matrix = []
        for row in ascii_string.split('\n'):
            matrix_row = []
            for char in row:
                if char not in '-o':
                    raise InvalidAsciiCharacterException(f"Found {char} character. Only `o` and `-` are allowed.")

                matrix_row.append(int(char == 'o'))
            matrix.append(matrix_row)
        print(ascii_string)  # TODO remove this print
        print(matrix)
        return matrix
