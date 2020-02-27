import pytest
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


def test_class_table_output():
    csv_string = StringIO("a,b,c\n1,123,12345\n")
    csv_table = csvtables.CSVTable(csv_string)
    output = csv_table.convert()
    assert (
        output
        == """| a | b   | c     |
| - | --- | ----- |
| 1 | 123 | 12345 |
"""
    )


def test_column_headers():
    csv_string = StringIO("a,b,c\n1,123,12345\n")
    csv_table = csvtables.CSVTable(csv_string)
    assert len(csv_table.columns) == 3


def test_column_header_names():
    csv_string = StringIO("a,b,c\n1,123,12345\n")
    csv_table = csvtables.CSVTable(csv_string)
    assert csv_table.columns[0].header == "a"
    assert csv_table.columns[1].header == "b"
    assert csv_table.columns[2].header == "c"


def test_class_header_names():
    csv_string = StringIO("a,b,c\n1,123,12345\n")
    csv_table = csvtables.CSVTable(csv_string)
    headers = csv_table.headers
    assert headers[0] == "a"
    assert headers[1] == "b"
    assert headers[2] == "c"


def test_class_set_header_names_wrong_number():
    csv_string = StringIO("a,b,c\n1,123,12345\n")
    csv_table = csvtables.CSVTable(csv_string)
    with pytest.raises(ValueError):
        csv_table.headers = ["only one"]


def test_class_set_header_names():
    csv_string = StringIO("a,b,c\n1,123,12345\n")
    csv_table = csvtables.CSVTable(csv_string)
    csv_table.headers = ["d", "e", "f"]
    headers = csv_table.headers
    assert headers[0] == "d"
    assert headers[1] == "e"
    assert headers[2] == "f"
