from io import StringIO
from csvtables import __version__
from csvtables import csvtables


def test_version():
    assert __version__ == "0.2.0"


def test_find_max_width():
    headers = ["a", "b", "c"]
    body = [{"a": "1", "b": "123", "c": "12345"}]
    col_max_width = csvtables.find_max_width(headers, body)
    assert col_max_width["a"] == 1
    assert col_max_width["b"] == 3
    assert col_max_width["c"] == 5


def test_table_output():
    csv_string = StringIO("a,b,c\n1,123,12345\n")
    output = csvtables.convert_table(csv_string)
    assert (
        output
        == """| a | b   | c     |
| - | --- | ----- |
| 1 | 123 | 12345 |
"""
    )
