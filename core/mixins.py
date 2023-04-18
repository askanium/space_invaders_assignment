from core.exceptions import InvalidAsciiCharacterException
from core.types import Frame
from maps.base import Map


class AsciiToBinaryMixin:

    @staticmethod
    def convert_ascii_to_binary_matrix(ascii_string: str) -> Frame:
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
            return Frame([])

        matrix = []
        for row in ascii_string.split('\n'):
            matrix_row = []
            for char in row:
                if char not in '-o':
                    raise InvalidAsciiCharacterException(f"Found {char} character. Only `o` and `-` are allowed.")

                matrix_row.append(int(char == 'o'))
            matrix.append(matrix_row)
        return Frame(matrix)


class BinaryToAsciiMixin:
    @staticmethod
    def convert_binary_matrix_to_ascii(binary_matrix: Frame) -> str:
        """
        Converts a binary matrix into an ASCII string based on the following characteristics:
        - "0" is converted into a dash "-"
        - "1" is converted into a circle "o"

        :param binary_matrix: The matrix to convert to ASCII string.
        :return: The converted ASCII string.
        """
        ascii_string = ''
        for row in binary_matrix:
            ascii_string = f"{ascii_string}{''.join('o' if bit else '-' for bit in row)}\n"
        return ascii_string


class DynamicProgrammingMixin:

    @staticmethod
    def compute_dp_matrix(map_: Map) -> list[list[int]]:
        """
        Compute the Dynamic Programming (DP) matrix in which each cell contains the cumulative
        number of signal bits (1s) of the frame that has (0,0) as the top left corner and
        the cell's coords as the bottom right corner.

        For instance, this map:

        1 0 1 1 0
        1 0 1 0 1
        1 1 0 0 1

        Will result in the following DP matrix:

        1 1 2 3 3
        2 2 4 5 6
        3 4 6 7 9

        :param map_: The map to process.
        :return: The DP populated matrix.
        """
        dp_matrix = []
        # create a longer list to simplify DP logic around first row
        dp_prev_row = [0] * (map_.width + 1)
        for row in map_.get_binary_representation():
            # create a longer list to simplify DP logic around first element
            dp_row = [0] * (len(row) + 1)
            cumulative_row = dp_row[:]  # make a copy

            for i, bit in enumerate(row):
                cumulative_row[i+1] = cumulative_row[i] + bit
                dp_row[i+1] = dp_prev_row[i + 1] + bit + cumulative_row[i]

            dp_matrix.append(dp_row[1:])
            dp_prev_row = dp_row

        return dp_matrix
