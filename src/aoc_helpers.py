def test_parse_digit_matrix():
    assert parse_digit_matrix("123\n456\n789") == [[1, 2, 3], [4, 5, 6], [7, 8, 9]]


def parse_digit_matrix(input_string):
    if not input_string:
        return []
    result = []
    for line in input_string.strip().split("\n"):
        result.append([int(char) for char in line.strip()])
    return result
